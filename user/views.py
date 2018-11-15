import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from .models import Profile
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ChangeAvatarForm


def login_modal(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        return JsonResponse({'status': 'SUCCESS'})
    else:
        return JsonResponse({'status': 'ERROR', 'msg': '用户名或密码错误'})


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
            profile = Profile.objects.create(user=user)
            profile.save()
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


def user_info(request):
    context = {}
    change_avatar_form = ChangeAvatarForm()
    context['change_avatar_form'] = change_avatar_form
    return render(request, 'user/user_info.html', context)


def change_nickname(request):
    user = request.user
    data = {}
    if not user.is_authenticated:
        data['code'] = 401
        data['message'] = '用户尚未登录!'
        data['status'] = 'ERROR'
        return JsonResponse(data)

    nickname = request.GET.get('nickname', '').strip()
    if nickname.strip() == '':
        data['code'] = 405
        data['message'] = '新昵称不能为空!'
        data['status'] = 'ERROR'
    else:
        user.profile.nickname = nickname
        user.profile.save()
        data['nickname'] = nickname
        data['status'] = 'SUCCESS'
    return JsonResponse(data)


def change_avatar(request):
    change_avatar_form = ChangeAvatarForm(request.POST, request.FILES, user=request.user)
    if change_avatar_form.is_valid():
        user = change_avatar_form.cleaned_data['user']
        avatar_dir = upload_avatar(change_avatar_form.cleaned_data['avatar'], user.username)        # save avatar
        user.profile.avatar.name = avatar_dir       # update avatar
        user.profile.save()
        return redirect(request.GET.get('from', reverse('home')))
    else:
        return redirect(request.GET.get('from', reverse('home')))


def upload_avatar(avatar, username):
    avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatar', username)      # create avatar file
    with open(avatar_dir, 'wb') as f:
        for chunk in avatar.chunks():
            f.write(chunk)
    return avatar_dir


def homepage(request, user_pk):
    user_ = get_object_or_404(User, pk=user_pk)
    blogs = user_.blog_set.all().order_by('-created_time')
    comments = user_.comments.all().order_by('-created_time')
    likes = user_.likerecord_set.all().order_by('-liked_time')

    context = {}
    context['user_'] = user_
    context['blogs'] = blogs
    context['comments'] = comments
    context['likes'] = likes

    return render(request, 'user/homepage.html', context)
