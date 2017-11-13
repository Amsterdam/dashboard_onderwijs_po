from rest_framework import viewsets
from rest_framework import routers

from dataset.models import Vestiging, LeerlingenNaarGewicht
from dataset.models import SchoolAdviezen
from api.serializers import VestigingSerializer, VestigingVizSerializer

from api.serializers import TempSerializer, SchoolAdviezenViz


class VestigingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vestiging.objects.all().order_by('brin').prefetch_related()
    serializer_class = VestigingSerializer

    filter_fields = ('brin6', 'naam', 'adres__stadsdeel')


class VestigingVizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Vestiging.objects.all()
        .order_by('brin')
        .prefetch_related()
        .select_related()
    )
    serializer_class = VestigingVizSerializer
    filter_fields = ('brin6', 'naam', 'adres__stadsdeel')


class OnderwijsAPIView(routers.APIRootView):
    """
    API endpoints voor primair onderwijs data sets.
    """


class OnderwijsAPIRouter(routers.DefaultRouter):
    APIRootView = OnderwijsAPIView


class VizAPIView(routers.APIRootView):
    """
    Custom API endpoints used for visualization purposes.
    """


class VizAPIRouter(routers.DefaultRouter):
    APIRootView = VizAPIView


class LeerlingenNaarGewichtViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LeerlingenNaarGewicht.objects.all()
    serializer_class = TempSerializer
    filter_fields = ('vestiging',)


class SchoolAdviezenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolAdviezen.objects.all()
    serializer_class = SchoolAdviezenViz
    filter_fields = ('vestiging',)
