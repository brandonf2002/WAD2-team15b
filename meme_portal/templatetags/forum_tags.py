from django import template
from django.shortcuts import get_object_or_404
from meme_portal.models import UserProfile

register = template.Library()

@register.simple_tag
def subtract(a, b):
    return a - b

@register.simple_tag
def add(a, b):
    return a + b

@register.simple_tag
def isIn(usr, mamyToManyRel):
    if not usr.is_authenticated:
        return False
    usrProf = get_object_or_404(UserProfile, user=usr)
    return usrProf in mamyToManyRel.all()
