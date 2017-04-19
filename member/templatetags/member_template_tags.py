from django import template
from member.models import BadgeAwards

register = template.Library()


@register.filter(name='getBadgeCount')
def getBadgeCount(list, key):
    if list and isinstance(list, dict):
        firstlist = list.get(key)
        return firstlist.get('count')


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')
