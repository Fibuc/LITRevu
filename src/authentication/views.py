from django.conf import settings
from django.contrib.auth import login, authenticate, logout 
from django.shortcuts import redirect, render

from . import forms

def login_user(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                message = f'Bonjour {user.username}, vous êtes connecté!'
                return redirect('home')
            else:
                message = 'Identifiant ou mot de passe invalide.'

    return render(request, 'authentication/login.html', {'form': form, 'message': message})

def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    form = forms.RegisterForm()
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        
    return render(request, 'authentication/register.html', {'form': form})


def home(request):
    return render(request, 'authentication/home.html')