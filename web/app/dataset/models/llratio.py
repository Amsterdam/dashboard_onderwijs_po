from django.db import models


class LeerlingLeraarRatio(models.Model):
    """Model to contain derived number Leerling Leraar Ratio"""
    class Meta:
        unique_together = ('brin', 'jaar')
    # Only BRIN code is present, not vestigingsnummer.
    brin = models.CharField(max_length=4)

    # extracted from Vestigingen table
    n_leerling = models.FloatField(null=True)

    # extracted from DUO CSV file
    n_directie = models.FloatField(null=True)
    n_onderwijzend = models.FloatField(null=True)
    n_ondersteunend = models.FloatField(null=True)
    n_inopleiding = models.FloatField(null=True)
    n_onbekend = models.FloatField(null=True)

    # denormalized city wide averages:
    n_onderwijzend_avg = models.FloatField(null=True)

    jaar = models.IntegerField()
