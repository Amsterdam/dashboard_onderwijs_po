from collections import defaultdict

from rest_framework import viewsets
from rest_framework import routers
from rest_framework.views import APIView
from rest_framework.response import Response

from dataset.models import Vestiging, LeerlingNaarGewicht, CitoScores
from dataset.models import SchoolAdvies, SchoolWisselaars, Subsidie, ToegewezenSubsidie
from dataset.models import LeerlingLeraarRatio
from api.serializers import VestigingSerializer
from api.serializers import CitoScoresSerializer
from api.serializers import SchoolWisselaarsSerializer
from api.serializers import SubsidieSerializer, ToegewezenSubsidieSerializer
from api.serializers import LeerlingLeraarRatioSerializer

from api.serializers import SchoolAdviesSerializer, LeerlingNaarGewichtSerializer


class VestigingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Vestiging.objects
        .select_related('adres')
        .prefetch_related('schooladvies_set')
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
        .order_by('id')
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
        .filter(vestiging__isnull=False)
        .select_related('vestiging')
        .select_related('advies')
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
        .order_by('id')
    )
    serializer_class = CitoScoresSerializer
    filter_fields = ('vestiging', 'jaar')


class SubsidieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Subsidie.objects.all()
    )
    serializer_class = SubsidieSerializer


class ToegewezenSubsidieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        ToegewezenSubsidie.objects
        .select_related('vestiging')
        .select_related('subsidie')
        .filter(vestiging__isnull=False)
        .order_by('id')
    )
    serializer_class = ToegewezenSubsidieSerializer
    filter_fields = ('vestiging', 'subsidie__jaar')


class SchoolWisselaarsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        SchoolWisselaars.objects
        .select_related('vestiging')
        .filter(vestiging__isnull=False)
    )
    serializer_class = SchoolWisselaarsSerializer
    filter_fields = ('vestiging', 'jaar')


class LeerlingLeraarRatioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LeerlingLeraarRatio.objects.all()
    serializer_class = LeerlingLeraarRatioSerializer
    filter_fields = ('brin', 'jaar')

# TODO: Move the aggregation logic below to the Vue.js presentation layer


class AggregatedAdviesView(APIView):
    def get(self, request, format=None):
        """
        For a given Vestiging (identified by BRIN6) aggregate the adviezen as specified.
        """
        brin6 = request.query_params.get('vestiging', None)
        if brin6 is None:
            return Response([])

        # add select_related (TODO)
        qs = (
            SchoolAdvies.objects
            .select_related('advies')
            .select_related('vestiging')  # check this
            .filter(vestiging=brin6)
        )

        mapping = defaultdict(dict)
        for obj in qs.all():
            mapping[obj.jaar][obj.advies.name] = obj.totaal

        out = []
        for jaar, adviezen in mapping.items():
            if jaar not in [2014, 2015, 2016]:
                continue  # for demo (which years to show is not yet specced)

            vmbo_bk = (
                adviezen.get('VMBO_BL_KL', 0) +
                adviezen.get('VMBO_KL', 0) +
                adviezen.get('VMBO_BL', 0)
            )
            pro_vso = (
                adviezen.get('PRO', 0) +
                adviezen.get('VSO', 0)
            )

            q, r = divmod(adviezen.get('VMBO_GT_HAVO', 0), 2)
            vmbo_gt = (
                adviezen.get('VMBO_GT', 0) +
                adviezen.get('VMBO_KL_GT', 0) +
                q +
                r
            )
            havo_vwo = (
                adviezen.get('HAVO_VWO', 0) +
                adviezen.get('HAVO', 0) +
                adviezen.get('VWO', 0) +
                q
            )

            out.extend([
                {
                    'advies': 'vmbo b,k',
                    'totaal': vmbo_bk,
                    'jaar': jaar,
                    'vestiging': brin6
                },
                {
                    'advies': 'havo / vwo',
                    'totaal': havo_vwo,
                    'jaar': jaar,
                    'vestiging': brin6
                },
                {
                    'advies': 'pro',
                    'totaal': pro_vso,
                    'jaar': jaar,
                    'vestiging': brin6
                },
                {
                    'advies': 'vmbo g,t',
                    'totaal': vmbo_gt,
                    'jaar': jaar,
                    'vestiging': brin6},
            ])

        return Response(out)
