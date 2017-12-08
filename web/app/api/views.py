from rest_framework import viewsets
from rest_framework import routers

from dataset.models import Vestiging, LeerlingNaarGewicht, CitoScores
from dataset.models import SchoolAdvies
from api.serializers import VestigingSerializer
from api.serializers import CitoScoresSerializer

from api.serializers import SchoolAdviesSerializer, LeerlingNaarGewichtSerializer


class VestigingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Vestiging.objects
        .select_related('adres')
        .prefetch_related('advies')
        .prefetch_related('cito_scores')
        .prefetch_related('leerling_naar_gewicht')
        .order_by('brin')
    )
    serializer_class = VestigingSerializer

    filter_fields = ('brin6', 'naam', 'adres__stadsdeel')


class OnderwijsAPIView(routers.APIRootView):
    """
    API endpoints voor primair onderwijs data sets.
    """


class OnderwijsAPIRouter(routers.DefaultRouter):
    APIRootView = OnderwijsAPIView


class LeerlingNaarGewichtViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        LeerlingNaarGewicht.objects
        .select_related('vestiging')
        .filter(vestiging__isnull=False)
    )
    serializer_class = LeerlingNaarGewichtSerializer
    filter_fields = ('vestiging',)


class SchoolAdviesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    School advies endpoint.

    Filterbaar op "vestiging".
    """
    # The filter is needed for SchoolAdviezen whose ForeignKey is null (we
    # cannot meaningfully display these).
    queryset = (
        SchoolAdvies.objects
        .select_related('vestiging')
        .select_related('advies')
        .filter(vestiging__isnull=False)
    )
    serializer_class = SchoolAdviesSerializer
    filter_fields = ('vestiging',)


class CitoScoresViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Cito scores endpoint.

    Filterbaar op "vestiging".
    """
    queryset = (
        CitoScores.objects
        .select_related('vestiging')
        .filter(vestiging__isnull=False)
    )
    serializer_class = CitoScoresSerializer
    filter_fields = ('vestiging',)
