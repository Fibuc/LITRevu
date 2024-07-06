from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect, render

from . import forms


def login_user(request):
    """Vue qui vérifie les informations de connection de l'utilisateur, et le connecte si elles sont valides.
    Sinon affiche un message d'erreur.

    Args:
        request (HttpRequest): Requête avec les informations de connection.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page principale.
    """
    # Bloque accès à la page d'authentification si l'utilisateur est déjà connecté.
    if request.user.is_authenticated:
        return redirect('feed')

    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                messages.error(request, 'Identifiant ou mot de passe invalide.')

    return render(request, 'authentication/login.html', {'form': form})


def logout_user(request):
    """Vue qui déconnecte l'utilisateur.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page de connexion ('login').
    """
    logout(request)
    return redirect('login')


def register_user(request):
    """Vue qui permet à l'utilisateur de s'enregistrer sur l'application si les données d'entrées sont valides.

    Args:
        request (HttpRequest): Requête avec les informations d'inscription.

    Returns:
        HttpResponse: Redirige l'utilisateur vers la page principale.
    """
    form = forms.RegisterForm()
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')

    return render(request, 'authentication/register.html', {'form': form})
