from rest_framework import serializers

from dataset import models


class AdresSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Adres
        exclude = ('id',)


class LeerlingenNaarGewichtSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeerlingenNaarGewicht
        fields = '__all__'


class SchoolAdviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolAdvies
        exclude = ('id', 'brin', 'vestigingsnummer')


class CitoScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CitoScores
        fields = '__all__'


class LeerlingLeraarRatio(serializers.ModelSerializer):
    class Meta:
        model = models.LeerlingLeraarRatio
        fields = '__all__'


class VestigingSerializer(serializers.ModelSerializer):
    adres = AdresSerializer()
    leerlingen_naar_gewicht = LeerlingenNaarGewichtSerializer(
        many=True, read_only=True)
    advies = SchoolAdviesSerializer(
        many=True, read_only=True)
    cito_scores = CitoScoresSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.Vestiging
        exclude = ('_id',)


# TODO: move this math to the serializer for SchoolAdvies
def school_advies_to_representation(instance):
    """
    Generate normalized
    """
    standard_fields = {
        'jaar': instance.jaar,
        'vestiging': instance.vestiging.brin6 if instance.vestiging else None
    }

    # Calculate the values for the various aggregations that were required.
    # Specifics as requested by the domain experts at Onderwijs.
    vmbo_bk = instance.vmbo_bl_kl + instance.vmbo_kl + instance.vmbo_bl
    pro_vso = instance.pro + instance.vso

    q, r = divmod(instance.vmbo_gt_havo, 2)
    assert r in [0, 1]
    vmbo_gt = instance.vmbo_gt + instance.vmbo_kl_gt + q + r
    havo_vwo = instance.havo_vwo + instance.havo + instance.vwo + q

    # Normalize the returned JSON (for use with Vega Lite). Note one record
    # in the database is mapped to several objects in JSON output.
    out = [
        {'advies': 'vmbo b,k', 'totaal': vmbo_bk},
        {'advies': 'h/v', 'totaal': havo_vwo},
        {'advies': 'pro & vso', 'totaal': pro_vso},
        {'advies': 'vmbo g,t', 'totaal': vmbo_gt}
    ]

    for record in out:
        record.update(standard_fields)
    return out


#  -- custom serializers for "Leerlingen naar gewicht" --

#  TODO: rename
#  TODO: check that all the select / prefetch related is active here
#  TODO: consider caching results ...

def lng_to_representation(instance):
    return [
        {
            "gewicht": "0.0",
            "totaal": instance.gewicht_0,
            "jaar": instance.jaar,
            "vestiging": instance.vestiging.brin6 if instance.vestiging else None
        },
        {
            "gewicht": "0.3",
            "totaal": instance.gewicht_0_3,
            "jaar": instance.jaar,
            "vestiging": instance.vestiging.brin6 if instance.vestiging else None
        },
        {
            "gewicht": "1.2",
            "totaal": instance.gewicht_1_2,
            "jaar": instance.jaar,
            "vestiging": instance.vestiging.brin6 if instance.vestiging else None
        }
    ]


class LNGVizListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        out = []
        for instance in data.all():
            out.extend(lng_to_representation(instance))

        return out


class LNGVizSerializer(serializers.Serializer):
    class Meta:
        models = models.LeerlingenNaarGewicht
        list_serializer_class = LNGVizListSerializer

    def to_representation(self, instance):
        # entries in database are not fully normalized, vega-lite does expect that
        return lng_to_representation(instance)


# -- full data set at once: --

class LeerlingenNaarGewichtVizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeerlingenNaarGewicht
        fields = ('gewicht_0', 'gewicht_0_3', 'gewicht_1_2', 'totaal', 'jaar', 'vestiging')


class CitoScoresVizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CitoScores
        exclude = ('id', 'brin', 'vestigingsnummer', 'vestiging')


class VestigingVizSerializer(serializers.ModelSerializer):
    # TODO: consider removing (not needed at the moment)
    leerlingen_naar_gewicht = LeerlingenNaarGewichtVizSerializer(
        many=True, read_only=True)
    school_adviezen = SchoolAdviesSerializer(
        many=True, read_only=True)
    cito_scores = CitoScoresVizSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.Vestiging
        fields = ('brin6', 'naam', 'leerlingen', 'leerlingen_naar_gewicht',
                  'school_adviezen', 'cito_scores')
