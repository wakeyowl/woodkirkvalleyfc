from django import template
from member.models import BadgeAwards

register = template.Library()


@register.inclusion_tag('member/my_badges.html')
def lookup(d, key):
    if d and isinstance(d, dict):
        return d.get(key)
