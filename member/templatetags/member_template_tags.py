from django import template
from django.contrib.auth.models import Group

register = template.Library()


# @register.filter(name='getBadgeCount')
# def getBadgeCount(list, key):
#     if list and isinstance(list, dict):
#         firstlist = list.get(key)
#         return firstlist.get('count')
#
#
# def cut(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, '')

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
