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


class SchoolAdviezenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolAdviezen
        fields = '__all__'


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
    school_adviezen = SchoolAdviezenSerializer(
        many=True, read_only=True)
    cito_scores = CitoScoresSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.Vestiging
        exclude = ('_id',)


# -- custom serializers for "Adviezen" bar chart --

def normalize(instance, fields, name_target, value_target):
    out = []
    for field in fields:
        out.append({
            name_target: field,
            value_target: getattr(instance, field)
        })
    return out


def school_advies_to_representation(instance):
    standard_fields = {
        'jaar': instance.jaar,
        'vestiging': instance.vestiging.brin6 if instance.vestiging else None
    }
    out = normalize(
        instance,
        [
            'vmbo_bl',
            'vmbo_bl_kl',
            'vmbo_gt',
            'vmbo_gt_havo',
            'vmbo_kl',
            'vmbo_kl_gt',
            'vso',
            'vwo'
        ],
        'advies',
        'totaal'
    )
    for record in out:
        record.update(standard_fields)
    return out


class SchoolAdviezenListViz(serializers.ListSerializer):
    def to_representation(self, data):
        out = []
        for instance in data.all():
            out.extend(school_advies_to_representation(instance))

        return out


class SchoolAdviezenViz(serializers.Serializer):
    class Meta:
        model = models.SchoolAdviezen
        list_serializer_class = SchoolAdviezenListViz

    def to_representation(self, instance):
        return school_advies_to_representation(instance)


#  -- custom serializers for "Leerlingen naar gewicht" --

#  TODO: mark as read only
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


class TempListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        out = []
        for instance in data.all():
            out.extend(lng_to_representation(instance))

        return out


class TempSerializer(serializers.Serializer):
    class Meta:
        models = models.LeerlingenNaarGewicht
        list_serializer_class = TempListSerializer

    def to_representation(self, instance):
        # entries in database are not fully normalized, vega-lite does expect that
        return lng_to_representation(instance)


# -- full data set at once: --

class LeerlingenNaarGewichtVizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeerlingenNaarGewicht
        fields = ('gewicht_0', 'gewicht_0_3', 'gewicht_1_2', 'totaal', 'jaar', 'vestiging')


class SchoolAdviezenVizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolAdviezen
        exclude = ('id', 'brin', 'vestigingsnummer', 'vestiging')


class CitoScoresVizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CitoScores
        exclude = ('id', 'brin', 'vestigingsnummer', 'vestiging')


class VestigingVizSerializer(serializers.ModelSerializer):
    leerlingen_naar_gewicht = LeerlingenNaarGewichtVizSerializer(
        many=True, read_only=True)
    school_adviezen = SchoolAdviezenVizSerializer(
        many=True, read_only=True)
    cito_scores = CitoScoresVizSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.Vestiging
        fields = ('brin6', 'naam', 'leerlingen', 'leerlingen_naar_gewicht',
                  'school_adviezen', 'cito_scores')
