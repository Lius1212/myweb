from django.contrib import admin
from .models import LikeRecord, OpposeRecord


@admin.register(LikeRecord)
class AdminLikeRecord(admin.ModelAdmin):
    list_display = ('content_object', 'user', 'liked_time')


@admin.register(OpposeRecord)
class AdminLikeRecord(admin.ModelAdmin):
    list_display = ('content_object', 'user', 'opposed_time')
