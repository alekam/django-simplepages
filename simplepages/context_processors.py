from simplepages.models import Page

def page(request):
    url = request.path
    if not url.startswith('/'):
        url = "/" + url

    try:
        page = Page.objects.get(url__exact=url)
    except:
        page = {}

    return {'page': page}
