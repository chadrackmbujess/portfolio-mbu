# portfolioapp/forms.py
from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre message'}),
        }

from django import forms
from .models import Comment, Reply

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # Seul le champ 'text' est nécessaire pour un commentaire

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']  # Seul le champ 'text' est nécessaire pour une réponse

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'bio', 'profile_picture', 'location',
            'date_of_birth', 'education_level', 'sex', 'activities', 'city', 'country', 'civil_status'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'activities': forms.Textarea(attrs={'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }