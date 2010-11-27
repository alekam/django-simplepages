from django.conf.urls.defaults import *

urlpatterns = patterns('simplepages.views',
    (r'^auto-url-prepend.js$', 'auto_url_prepend_js'),
)
