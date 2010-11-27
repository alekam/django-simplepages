from django.http import Http404
from django.conf import settings

from simplepages.views import page


class PageFallbackMiddleware(object):

    def process_response(self, request, response):
        if response.status_code != 404:
            return response # no need to check for a flatpage for non-404 responses.

        try:
            return page(request, request.path)
        # return the original response if any errors happened; because this
        # is a middleware, we can't assume the errors will be caught elsewhere
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
