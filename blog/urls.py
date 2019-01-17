from django.urls import path
from . import views

urlpatterns = [
        path('', views.blog_list, name='blog_list'),
        path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
        path('type/<int:blog_type_pk>', views.blog_with_type, name='blog_with_type'),
        path('date/<int:year>/<int:month>', views.blog_with_date, name='blog_with_date'),
        path('author/<int:author_pk>', views.blog_with_author, name='blog_with_author'),
        path('blog_search/', views.blog_search, name='blog_search'),
    ]
