from django import forms
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class UserSearchForm(forms.Form):
    placeholder = forms.TextInput(attrs={'placeholder': 'Rechercher un utilisateur'})
    search_user = forms.CharField(widget=placeholder, max_length=63, label='', required=False)


class FollowForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['followings']


class TicketForm(forms.ModelForm):
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
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']
        widgets = {
            'rating': forms.NumberInput(attrs={'placeholder': 'Note de 1 à 5'}),
            'headline': forms.TextInput(attrs={'placeholder': 'Titre de la critique'}),
            'body': forms.Textarea(attrs={'placeholder': 'Critique'})
        }
        labels = {
            'rating': '',
            'headline': '',
            'body': '',
        }