from django.db import models


class Adres(models.Model):
    """Shadow the adress as defined by schoolwijzer.amsterdam.nl"""
    adres = models.CharField(max_length=255)
    email = models.EmailField()
    plaats = models.CharField(max_length=255)
    postcode = models.CharField(max_length=6)
    stadsdeel = models.CharField(max_length=255)
    telefoon = models.CharField(max_length=15)
    website = models.URLField()


class VestigingManager(models.Manager):
    def _from_schoolwijzer_json_enty(self, json_dict):
        pass  # TODO implement


class Vestiging(models.Model):
    """Shadow the Vestiging as defined by schoolwijzer.amsterdam.nl"""
    class Meta:
        unique_together = ('brin', 'vestigingsnummer')

    adres = models.ForeignKey(Adres)
    brin = models.CharField(max_length=4)
    lat = models.FloatField()
    lon = models.FloatField()
    grondslag = models.CharField(max_length=255)
    heeft_voorschool = models.BooleanField()
    _id = models.IntegerField()  # TODO: investigate: can be primary key?
    leerlingen = models.IntegerField()
    naam = models.CharField(max_length=255)
    onderwijsconcept = models.CharField(max_length=255, null=True)
    schoolwijzer_url = models.URLField()
    vestigingsnummer = models.IntegerField(null=True)

    brin6 = models.CharField(max_length=6, primary_key=True)
    gebiedscode = models.CharField(max_length=4)
