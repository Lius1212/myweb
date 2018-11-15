from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField(null=False)
    created_time = models.DateTimeField(auto_now_add=True)

    commentator = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    # 父级评论
    parent = models.ForeignKey('self', null=True, related_name='parent_comments', on_delete=models.CASCADE)
    # 回复的对象
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)
    # 根级评论
    root = models.ForeignKey('self', null=True, related_name='root_comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['created_time']
