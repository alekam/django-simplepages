import re
from datetime import datetime

from django import template
from django.template import resolve_variable
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe, SafeData
from django.utils.html import linebreaks

from simplepages.models import Page, SiteSection

HTML_RE = re.compile('<br>|<br />|<p>|<table>', re.IGNORECASE)
register = template.Library()


@register.inclusion_tag('pages/main_menu.html')
def main_menu(request):
    main_menu = SiteSection.objects.menu_items()
    for menu in main_menu:
        if menu.url != '/':
            if request.path.find(menu.url) >= 0:
                menu.current = True
            else:
                menu.current = False

    return {'main_menu': main_menu}


@register.inclusion_tag('pages/top_menu.html')
def top_menu(request):
    main_menu = SiteSection.objects.menu_items()
    for menu in main_menu:
        if menu.url != '/':
            if request.path.find(menu.url) >= 0:
                menu.current = True
            else:
                menu.current = False

    return {'main_menu': main_menu}


def autolinebreaks(value, autoescape=None):
    """Check if the content is HTML or plain text. If plain text, then
    replace line breaks with the appropriate HTML. A single newline
    becomes an HTML line break (`<br />`) and a new line followed by a
    blank line becomes a paragraph break (`</p>`).
    """
    if not HTML_RE.search(value):
        autoescape = autoescape and not isinstance(value, SafeData)
        return mark_safe(linebreaks(value, autoescape))
    else:
        return value

autolinebreaks.is_safe = True
autolinebreaks.needs_autoescape = True
autolinebreaks = stringfilter(autolinebreaks)
register.filter(autolinebreaks)
