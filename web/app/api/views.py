from rest_framework import viewsets
from rest_framework import routers

from dataset.models import Vestiging, LeerlingenNaarGewicht
from dataset.models import SchoolAdviezen
from api.serializers import VestigingSerializer, VestigingVizSerializer

from api.serializers import LNGVizSerializer, SchoolAdviezenViz


class VestigingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Vestiging.objects
        .select_related('adres')
        .prefetch_related('school_adviezen')
        .prefetch_related('cito_scores')
        .prefetch_related('leerlingen_naar_gewicht')
        .order_by('brin')
    )
    serializer_class = VestigingSerializer

    filter_fields = ('brin6', 'naam', 'adres__stadsdeel')


class VestigingVizViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: consider removing this endpoint for now (Something like this is
    # needed by a future JavaScript front-end that can cache the whole data
    # set at the client side for performance).
    queryset = (
        Vestiging.objects.all()
        .order_by('brin')
        .select_related('adres')
        .prefetch_related('school_adviezen')
        .prefetch_related('cito_scores')
        .prefetch_related('leerlingen_naar_gewicht')
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
    queryset = (
        LeerlingenNaarGewicht.objects
        .select_related('vestiging')
    )
    serializer_class = LNGVizSerializer
    filter_fields = ('vestiging',)


class SchoolAdviezenViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint voor "School adviezen" visualisatie.

    Dit endpoint is filterbaar op 'vestiging' veld (BRIN6).
    """
    # The filter is needed for SchoolAdviezen whose ForeignKey is null (we
    # cannot meaningfully display these).
    queryset = (
        SchoolAdviezen.objects
        .select_related('vestiging')
        .filter(vestiging__isnull=False)
    )
    serializer_class = SchoolAdviezenViz
    filter_fields = ('vestiging',)
