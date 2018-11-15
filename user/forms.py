from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            self.cleaned_data['user'] = user
            return self.cleaned_data
        else:
            raise forms.ValidationError('用户名或密码错误')


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', min_length=3, max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入新的用户名'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(label='新的密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}))
    password_again = forms.CharField(label='再次输入新的密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请再次输入新的密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        else:
            return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次密码输入不一致')
        else:
            return password_again


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧的密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入旧的密码'}))
    new_password = forms.CharField(label='新的密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}))
    new_password_again = forms.CharField(label='再次输入新的密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '请再次输入新的密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password_again(self):
        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_password_again']
        if new_password != new_password_again:
            raise forms.ValidationError('两次密码输入不一致')
        else:
            return new_password_again

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('原密码输入错误')
        else:
            return old_password


class ChangeAvatarForm(forms.Form):
    avatar = forms.FileField(label='')

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeAvatarForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user:
            self.cleaned_data['user'] = self.user
        return self.cleaned_data

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar.size > 2 * 2 ** 20:         # > 2mb
            raise forms.ValidationError('上传头像文件过大')
        # judge format
        if avatar.name.endswith(('.jpg', '.png', '.bmp', '.jpeg')):
            return avatar

        raise forms.ValidationError('上传头像格式错误')
