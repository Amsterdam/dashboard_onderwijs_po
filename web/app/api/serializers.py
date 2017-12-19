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
