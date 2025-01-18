from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Modèle Category
class Category(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.name

# Modèle Project
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="Chadrack Mbu Jess")
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.title

# Modèle Comment
class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Créer une notification pour l'auteur du projet (sauf si c'est lui qui commente)
        if self.project.user != self.author:
            Notification.objects.create(
                user=self.project.user,
                message=f"{self.author.username} a commenté votre projet : {self.project.title}",
                link=f"/projects/{self.project.id}/"
            )

# Modèle Reply
class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Créer une notification pour l'auteur du commentaire (sauf si c'est lui qui répond)
        if self.comment.author != self.author:
            Notification.objects.create(
                user=self.comment.author,
                message=f"{self.author.username} a répondu à votre commentaire sur le projet : {self.comment.project.title}",
                link=f"/projects/{self.comment.project.id}/"
            )
# Modèle Notification
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

    def mark_as_read(self):
        """Marque la notification comme lue."""
        if not self.is_read:
            self.is_read = True
            self.save()

# Modèle Profile
class Profile(models.Model):
    SEX_CHOICES = [('M', 'Masculin'), ('F', 'Féminin'), ('O', 'Autre')]
    CIVIL_STATUS_CHOICES = [('S', 'Célibataire'), ('M', 'Marié(e)'), ('D', 'Divorcé(e)'), ('W', 'Veuf/Veuve')]
    EDUCATION_LEVEL_CHOICES = [('P', 'Primaire'), ('S', 'Secondaire'), ('B', 'Baccalauréat'), ('L', 'Licence'), ('M', 'Master'), ('D', 'Doctorat')]

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Photo de profil")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nom complet")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True, verbose_name="Sexe")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS_CHOICES, blank=True, null=True, verbose_name="État civil")
    activities = models.TextField(blank=True, null=True, verbose_name="Activités")
    education_level = models.CharField(max_length=1, choices=EDUCATION_LEVEL_CHOICES, blank=True, null=True, verbose_name="Niveau d'études")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Localisation")
    country = CountryField(blank=True, null=True, verbose_name="Pays", default='FR')
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ville")

    def __str__(self):
        return f"Profil de {self.user.username}"

# Signaux pour créer/sauvegarder un profil automatiquement
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Modèle Skill
class Skill(models.Model):
    title = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"

    def __str__(self):
        return self.title

# Modèle Contact
class Contact(models.Model):
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email

# Modèle About
class About(models.Model):
    description = RichTextField(verbose_name="Description")
    photo = models.ImageField(upload_to='about/', verbose_name="Photo de profil")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return "À propos de moi"

    class Meta:
        verbose_name = "À propos"
        verbose_name_plural = "À propos"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Blog")
        verbose_name_plural = ("Blogs")

    def __str__(self):
        return self.title