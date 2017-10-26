from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^onderwijs/admin/', admin.site.urls),
    url(r'^status/', include('health.urls', namespace='health')),
]
