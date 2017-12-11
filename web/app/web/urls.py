from django.conf.urls import url
from django.views.generic import TemplateView

from .views import VestigingListView, VestigingDetailView

urlpatterns = [
    url(r'^demo/$', TemplateView.as_view(template_name='web/demo.html')),
    url(
        r'^vestiging/$',
        VestigingListView.as_view(template_name='web/vestiging_list.html')
    ),
    url(
        r'^vestiging/(?P<pk>[0-9]{2}[A-Z]{2}[0-9]{2})/$',
        VestigingDetailView.as_view(template_name='web/vestiging_detail.html')
    ),
]
