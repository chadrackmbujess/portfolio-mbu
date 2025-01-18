# Generated by Django 5.1.4 on 2025-01-17 21:34

import ckeditor.fields
import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('photo', models.ImageField(upload_to='about/', verbose_name='Photo de profil')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
            ],
            options={
                'verbose_name': 'À propos',
                'verbose_name_plural': 'À propos',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog_images/')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Catégories',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Compétance',
                'verbose_name_plural': 'Compétances',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('link', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/', verbose_name='Photo de profil')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom complet')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Masculin'), ('F', 'Féminin'), ('O', 'Autre')], max_length=1, null=True, verbose_name='Sexe')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Bio')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date de naissance')),
                ('civil_status', models.CharField(blank=True, choices=[('S', 'Célibataire'), ('M', 'Marié(e)'), ('D', 'Divorcé(e)'), ('W', 'Veuf/Veuve')], max_length=1, null=True, verbose_name='État civil')),
                ('activities', models.TextField(blank=True, null=True, verbose_name='Activités')),
                ('education_level', models.CharField(blank=True, choices=[('P', 'Primaire'), ('S', 'Secondaire'), ('B', 'Baccalauréat'), ('L', 'Licence'), ('M', 'Master'), ('D', 'Doctorat')], max_length=1, null=True, verbose_name="Niveau d'études")),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Localisation')),
                ('country', django_countries.fields.CountryField(blank=True, default='FR', max_length=2, null=True, verbose_name='Pays')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ville')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='projects/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolioapp.category')),
                ('user', models.ForeignKey(default='Chadrack Mbu Jess', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Projet',
                'verbose_name_plural': 'Projets',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='portfolioapp.project')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='portfolioapp.comment')),
            ],
        ),
    ]
