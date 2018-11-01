from django import template
from ..models import Profile

register = template.Library()


@register.simple_tag
def get_nickname_or_username(user):
    profile = Profile.objects.get(user=user)
    if profile.nickname:
        return profile.nickname
    else:
        return user.username
