from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm
from blog.models import Blog

register = template.Library()


@register.simple_tag
def get_comments_list(obj):
    ct = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=ct, object_id=obj.pk, parent=None).order_by('created_time')


@register.simple_tag
def get_comment_form(obj):
    ct = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type': ct.model, 'object_id': obj.pk, 'reply_comment_id': 0})
    return form


@register.simple_tag
def get_comments_num(obj):
    ct = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=ct, object_id=obj.pk).count()


@register.simple_tag
def get_comment_to(obj):
    # 评论博客
    if obj.parent is None:
        return Blog.objects.get(id=obj.object_id)
    # 评论回复/评论
    else:
        blog = Blog.objects.get(id=obj.object_id)
        parent = obj.parent
        return blog, parent
