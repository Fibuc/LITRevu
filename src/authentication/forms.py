from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username']

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
        label='')

    password = forms.CharField(
        max_length=63,
        widget=forms.TextInput(
            attrs={'placeholder': "Nom d'utilisateur",'type': "password"}
        ),
        label='')