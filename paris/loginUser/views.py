from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from . import forms
from .models import customUser

def login_page(request):
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
                return redirect('profil')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'login.html', context={'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'signup.html', context={'form': form})


def home_page(request):

    return render(request, 'home.html')


def leaderboard_page(request):
    competiteurs = customUser.objects.all().order_by("-recompense")

    return render(request, 'leaderboard.html', context={'classement': competiteurs})


def rules_page(request):
    return render(request, 'rules.html')


@login_required
def userAccount(request):
    competiteurs = customUser.objects.all().order_by("-recompense")
    totalComp = len(competiteurs)
    currentUser = request.user.pk
    place = 0

    for comp in competiteurs:
        place = place+1
        if comp.pk == currentUser:
            break

    return render(request, 'profil.html', context={'totalComp': totalComp, 'place': place})