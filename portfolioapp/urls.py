from django.urls import path
from . import views
from .views import custom_logout, get_unread_notifications_count, view_notifications, mark_all_notifications_as_read, mark_notification_as_read

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('projects/', views.projects_view, name='projects'),
    path('projets/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail_en'),
    path('projets/<int:project_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', custom_logout, name='logout'),
    path('unread-notifications/', get_unread_notifications_count, name='unread_notifications'),
    path('notifications/', view_notifications, name='view_notifications'),
    path('notification/mark-as-read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('mark-all-notifications-as-read/', mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]