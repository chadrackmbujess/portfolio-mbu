from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Comment, Reply, Notification, Category, About
from .forms import CommentForm, ReplyForm, ProfileForm

def home(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'portfolioapp/home.html', {'projects': projects})

def blog(request):
    return render(request, 'portfolioapp/blog.html')

def projects_view(request):
    projects = Project.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    category_icons = {
        "Développement": "bi-code",
        "Design": "bi-brush",
        "Marketing": "bi-megaphone",
        "IA": "bi-cpu",
        "Gestion de Base de données": "bi-database",
        "Automatisation": "bi-robot",
        "Ecole": "bi-building",
        "Portfolio": "bi-briefcase",
        "App Desktop": "bi-laptop",
        "App Web": "bi-globe",
        "Aide": "bi-life-preserver",
        "Eglise": "bi-house-door",
        "TV": "bi-tv",
    }
    category_filter = request.GET.get('category')
    if category_filter:
        if category_filter == 'all':
            pass
        elif category_filter == 'uncategorized':
            projects = projects.filter(category__isnull=True)
        else:
            try:
                category_id = int(category_filter)
                projects = projects.filter(category_id=category_id)
            except ValueError:
                pass
    for project in projects:
        if not project.image:
            project.image_url = '/static/images/default.jpg'
        else:
            project.image_url = project.image.url
    return render(request, 'portfolioapp/projects.html', {
        'projects': projects,
        'categories': categories,
        'category_icons': category_icons,
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    categories = Category.objects.all()
    categories_with_projects = [category for category in categories if Project.objects.filter(category=category).exists()]
    projects_by_category = {category: Project.objects.filter(category=category) for category in categories_with_projects}
    uncategorized_projects = Project.objects.filter(category__isnull=True)
    if uncategorized_projects.exists():
        projects_by_category["non_categorise"] = uncategorized_projects
    return render(request, 'portfolioapp/project_detail.html', {
        'project': project,
        'projects_by_category': projects_by_category,
        'categories': categories_with_projects,
    })

@login_required
def add_comment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.author = request.user
            comment.save()
            return redirect('project_detail', pk=project.id)
    else:
        form = CommentForm()
    return render(request, 'project_detail.html', {'form': form})

@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.author = request.user
            reply.save()
            return redirect('project_detail', pk=comment.project.id)
    else:
        form = ReplyForm()
    return render(request, 'project_detail.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username} ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'registration/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'registration/edit_profile.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def get_unread_notifications_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})

@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'portfolioapp/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.mark_as_read()
    return redirect(notification.link)

@login_required
def mark_all_notifications_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('view_notifications')

def about(request):
    about_info = About.objects.first()
    return render(request, 'portfolioapp/about.html', {'about_info': about_info})

def contact(request):
    return render(request, 'portfolioapp/contact.html')