"""
Models for various external data sources.
"""
# TODO items:
# * How far will we go in modelling our data, how to re-use what is
#   available already in API form at Datapunt (regarding adres and
#   gebiedscode).
# * Is a reference to schoolwijzer enough at run time?
# * Figure out how to handle jaar or peildatum
# * consider DecimalField s
from django.db import models


# -- from schoolwijzer --
class Adres(models.Model):
    """Shadow the adress as defined by schoolwijzer.amsterdam.nl"""
    adres = models.CharField(max_length=255)
    email = models.EmailField()
    plaats = models.CharField(max_length=255)
    postcode = models.CharField(max_length=6)
    stadsdeel = models.CharField(max_length=255)
    telefoon = models.CharField(max_length=15)
    website = models.URLField()


class Vestiging(models.Model):
    """Shadow the Vestiging as defined by schoolwijzer.amsterdam.nl"""
    # TODO: talk to experts; how are moves/openings/closings handled?
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
    vestigingsnummer = models.IntegerField()


# -- from DUO web APIs and CSV dump

class LeerlingenNaarGewicht(models.Model):
    """Shadow relevant part of Leerling naar gewicht dataset of DUO."""
    # TODO: base links on the following (or build a BRIN 6 code)
    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    # relevant (subset) of properties
    # TODO: consider DecimalField
    gewicht_0 = models.FloatField()
    gewicht_0_3 = models.FloatField()
    gewicht_1_2 = models.FloatField()

    # TODO: add peildatum (also jaar seperately)


class SchoolAdviezen(models.Model):
    """Shadow relevant parst of School Adviezen dataset of DUO."""
    # TODO: base links on the following (or build a BRIN 6 code)
    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    # relevant (subset) of properties
    vmbo_bl = models.IntegerField()
    vmbo_bl_kl = models.IntegerField()
    vmbo_gt = models.IntegerField()
    vmbo_gt_havo = models.IntegerField()
    vmbo_kl = models.IntegerField()
    vmbo_kl_gt = models.IntegerField()
    vso = models.IntegerField()
    vwo = models.IntegerField()

    # TODO: ga na wat 'PRO' betekend; school advies?
    # TODO: PEILDATUM_ADVIEZEN PEILDATUM_LEERLINGEN


class CitoScores(models.Model):
    """Shadow relevant parst of CITO Scores dataset of DUO."""
    # TODO: base links on the following (or build a BRIN 6 code)
    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    # relevant:
    # TODO: talk to experts about meaning of fields in DUO data
    # TODO: peildatum etc.
    cet_gem = models.FloatField()
    leerjaar_8 = models.IntegerField()


class LeerlingLeraarRatio(models.Model):
    """Model to contain derived number Leerling Leraar Ratio"""
    # TODO: base links on the following (or build a BRIN 6 code)
    brin = models.CharField(max_length=4)
#    vestigingsnummer = models.IntegerField()  # Not present in source

    #
    ratio = models.FloatField()

