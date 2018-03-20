from rest_framework import serializers

from dataset import models

from datapunt_api.rest import HALSerializer


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


class AdresSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Adres
        exclude = ('id',)


class VestigingSerializer(HALSerializer):
    # Note: used both for list and detail views in viewset.
    # Note: lookup_field defaults to model primary key (here: brin6)
    adres = AdresSerializer()
    leerling_naar_gewicht = LeerlingNaarGewichtSerializer(
        many=True, read_only=True)
    cito_scores = CitoScoresSerializer(
        many=True, read_only=True)
    schooladvies_set = SchoolAdviesSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.Vestiging
        fields = (
            '_links',
            'brin6',
            'adres',
            'leerling_naar_gewicht',
            'cito_scores',
            'schooladvies_set',
            'brin',
            'lat',
            'lon',
            'grondslag',
            'heeft_voorschool',
            'leerlingen',
            'naam',
            'onderwijsconcept',
            'schoolwijzer_url',
            'vestigingsnummer',
            'gebiedscode'
        )


class LeerlingLeraarRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeerlingLeraarRatio
        exclude = ('id',)
