from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.fields import ContentType
from ..models import LikeCount, LikeRecord, OpposeCount, OpposeRecord
from blog.models import Blog
from comment.models import Comment

register = template.Library()


@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model


@register.simple_tag
def get_likes_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return like_count.likes_num


@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'text-danger'
    else:
        return ''


@register.simple_tag
def get_oppose_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    oppose_count, created = OpposeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return oppose_count.opposes_num


@register.simple_tag(takes_context=True)
def get_oppose_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if OpposeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'text-danger'
    else:
        return ''


@register.simple_tag
def get_like_to(obj):
    model_class = obj.content_type.model_class()   # Blog/ Comment
    if model_class == Blog:
        return model_class.objects.get(id=obj.object_id)
    elif model_class == Comment:
        comment = model_class.objects.get(id=obj.object_id)
        blog = Blog.objects.get(id=comment.object_id)
        return blog, comment
    else:
        raise ObjectDoesNotExist('No type for liked')
