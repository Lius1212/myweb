from django.urls import path
from . import views

urlpatterns = [
    path('like_change/', views.like_change, name='like_change'),
    path('oppose_change/', views.oppose_change, name='oppose_change'),
]

