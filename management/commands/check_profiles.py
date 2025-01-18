from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolioapp.models import Profile

class Command(BaseCommand):
    help = 'Vérifie et crée les profils manquants pour tous les utilisateurs'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Profil créé pour {user.username}'))