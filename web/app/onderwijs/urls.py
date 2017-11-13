from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from api import views, urls
from api import urls as api_urls

urlpatterns = [
    url(r'^status/', include('health.urls', namespace='health')),
    url(r'^onderwijs/', include(api_urls.onderwijs_router.urls)),
]
