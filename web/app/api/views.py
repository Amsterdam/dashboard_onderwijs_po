from rest_framework import viewsets
from rest_framework import routers

from dataset.models import Vestiging, LeerlingenNaarGewicht
from dataset.models import SchoolAdviezen
from api.serializers import VestigingSerializer, VestigingVizSerializer

from api.serializers import LNGVizSerializer, SchoolAdviezenViz


class VestigingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vestiging.objects.all().order_by('brin').prefetch_related()
    serializer_class = VestigingSerializer

    filter_fields = ('brin6', 'naam', 'adres__stadsdeel')


class VestigingVizViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: consider removing this endpoint for now (Something like this is
    # needed by a future JavaScript front-end that can cache the whole data
    # set at the client side for performance).
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


class LeerlingenNaarGewichtViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint voor "Leerlingen naar gewicht" visualisatie.

    Dit endpoint is filterbaar op 'vestiging' veld (BRIN6).
    """
    queryset = LeerlingenNaarGewicht.objects.all()
    serializer_class = LNGVizSerializer
    filter_fields = ('vestiging',)


class SchoolAdviezenViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint voor "School adviezen" visualisatie.

    Dit endpoint is filterbaar op 'vestiging' veld (BRIN6).
    """
    queryset = SchoolAdviezen.objects.all()
    serializer_class = SchoolAdviezenViz
    filter_fields = ('vestiging',)
