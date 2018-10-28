from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegisterForm, ChangePasswordForm


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegisterForm()

    context = {}
    context['register_form'] = register_form
    return render(request, 'user/register.html', context)


def change_password(request):
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST, user=request.user)
        if change_password_form.is_valid():
            user = request.user
            new_password = change_password_form.cleaned_data['new_password_again']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        change_password_form = ChangePasswordForm()

    context = {}
    context['change_password_form'] = change_password_form
    return render(request, 'user/change_password.html', context)

