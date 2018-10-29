from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


@register.simple_tag
def get_comments_list(obj):
    ct = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=ct, object_id=obj.pk).order_by('created_time')


@register.simple_tag
def get_comment_form(obj):
    ct = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type': ct.model, 'object_id': obj.pk})
    return form
