from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('change_password/', views.change_password, name='change_password'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
]
