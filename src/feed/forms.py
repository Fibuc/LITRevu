from django import forms
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class UserSearchForm(forms.Form):
    """Formulaire de recherche des utilisateurs"""
    placeholder = forms.TextInput(attrs={'placeholder': 'Rechercher un utilisateur'})
    search_user = forms.CharField(widget=placeholder, max_length=63, label='', required=False)


class FollowForm(forms.ModelForm):
    """Formulaire de suivi des utilisateurs."""
    class Meta:
        model = User
        fields = ['followings']


class TicketForm(forms.ModelForm):
    """Formulaire de création de ticket."""
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre livre/article'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'})
        }
        labels = {
            'title': '',
            'description': '',
            'image': '',
        }


class ReviewForm(forms.ModelForm):
    """Formulaire de création de critique."""
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'rating': forms.RadioSelect(),
            'headline': forms.TextInput(attrs={'placeholder': 'Titre de la critique'}),
            'body': forms.Textarea(attrs={'placeholder': 'Critique'})
        }
        labels = {
            'rating': '',
            'headline': '',
            'body': '',
        }
