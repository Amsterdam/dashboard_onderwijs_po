from django.conf.urls import url, include
from django.conf import settings

from api import urls as api_urls
from health import urls as health_urls

urlpatterns = [
    url(r'^status/', include(health_urls)),
    url(r'^onderwijs/api/', include(api_urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
