import re
from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'id', 'content_', 'commentator', 'created_time')

    @staticmethod
    def content_(obj):
        return re.sub('<.*?>', '', obj.content)
