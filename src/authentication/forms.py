from authentication.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    """Formulaire d'inscription personnalisé basé sur UserCreationForm."""
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer mot de passe'}))

    class Meta(UserCreationForm.Meta):
        """
        Classe qui hérite des métadonnées de UserCreationForm.Meta afin de spécifier les champs à inclure dans le
        formulaire.
        """
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"})
        }

    def clean_password2(self):
        """
        Cette méthode vérifie que les deux mots de passe saisis (password1 et password2) correspondent.
        Si les mots de passe ne correspondent pas, une ValidationError est levée.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2


class LoginForm(forms.Form):
    """Formulaire de connexion utilisateur."""
    username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
        label='')

    password = forms.CharField(
        max_length=63,
        widget=forms.TextInput(
            attrs={'placeholder': "Mot de passe", 'type': "password"}
        ),
        label='')
