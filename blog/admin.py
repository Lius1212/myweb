from django.contrib import admin
from .models import BlogType, Blog


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'created_time', 'update_time')
    list_editable = ('title', 'blog_type', 'author')
    list_filter = ('blog_type', 'author',)
    search_fields = ('title', 'content')
