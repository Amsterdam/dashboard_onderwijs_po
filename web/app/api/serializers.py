from rest_framework import serializers

from dataset import models


class AdresSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Adres
        exclude = ('id',)


class LeerlingNaarGewichtSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeerlingNaarGewicht
        exclude = ('id', 'brin', 'vestigingsnummer')


class SchoolAdviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolAdvies
        exclude = ('id', 'brin', 'vestigingsnummer')


class CitoScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CitoScores
        exclude = ('id', 'brin', 'vestigingsnummer')


class LeerlingLeraarRatio(serializers.ModelSerializer):
    class Meta:
        model = models.LeerlingLeraarRatio
        fields = '__all__'


class SubsidieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subsidie
        exclude = ('id',)


class ToegewezenSubsidieSerializer(serializers.ModelSerializer):
    subsidie = serializers.SerializerMethodField()

    def get_subsidie(self, obj):
        return obj.subsidie.naam

    class Meta:
        model = models.ToegewezenSubsidie
        exclude = ('id',)


class SchoolWisselaarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolWisselaars
        exclude = ('id', 'brin', 'vestigingsnummer')


class VestigingSerializer(serializers.ModelSerializer):
    adres = AdresSerializer()
    leerling_naar_gewicht = LeerlingNaarGewichtSerializer(
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
