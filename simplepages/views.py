from django.core.xheaders import populate_xheaders
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings

from simplepages.models import Page, SiteSection

DEFAULT_TEMPLATE = 'pages/default.html'


def page(request, url):
    """Page view.

    Models: `simplepages.page`
    Templates: Uses the template defined by the `template_name` field,
        or `staticpages/default.html` if template_name is not defined.
    """
    if not url.startswith('/'):
        url = "/" + url
    
    # Fix as the APPEND_SLASH setting doesn't work with
    # the flatpages/simplepages app
    try:
        f = Page.objects.get(url__exact=url)    
    except ObjectDoesNotExist:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url = url + '/'
            f = get_object_or_404(Page, url__exact=url)
        else:
            raise Http404

    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)

    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    c = RequestContext(request, {
        'page': f,
        'request': request,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, Page, f.id)

    return response


def auto_url_prepend_js(request):
    sections = SiteSection.objects.all()
    c = RequestContext(request, {
        'sections': sections,
        })
    t = loader.get_template('pages/auto_url_prepend.js')
    response = HttpResponse(t.render(c), mimetype='application/javascript')

    return response
