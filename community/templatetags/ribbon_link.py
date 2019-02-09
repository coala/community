from django import template
from community.git import get_remote_url


register = template.Library()


@register.simple_tag
def get_ribbon_link():
    url = get_remote_url()
    link = 'https://' + url.resource + '/' + url.pathname
    return link
