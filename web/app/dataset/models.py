"""
Models for various external data sources.
"""
# flake8: noqa
# TODO items:
# * consider DecimalField s
# * once information model is settled, refactor
import collections
import requests
import pandas
from openpyxl import load_workbook

from datetime import datetime

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


class VestigingManager(models.Manager):
    def _from_schoolwijzer_json_enty(self, json_dict):
        pass


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


# -- from DUO web APIs and CSV dump

class DUOAPIManagerMixin:
    def from_duo_api_json(self, data, year, brin6s):
        instances = []
        for entry in data['results']:
            instances.append(self._from_duo_api_json_entry(entry, year, brin6s))
        self.bulk_create(instances)


class LeerlingenNaarGewichtManager(models.Manager, DUOAPIManagerMixin):
    def _from_duo_api_json_entry(self, json_dict, year, brin6s):
        # Note: somehow self.create( ... ) leads to problems with bulk_create.

        brin6 = brin=json_dict['BRIN_NUMMER'] + \
            '{:02d}'.format(int(json_dict['VESTIGINGSNUMMER']))

        peildatum = datetime.strptime(json_dict['PEILDATUM'], '%Y%m%d')

        obj = LeerlingenNaarGewicht(
            brin=json_dict['BRIN_NUMMER'],
            vestigingsnummer=json_dict['VESTIGINGSNUMMER'],

            gewicht_0=json_dict['GEWICHT_0'],
            gewicht_0_3=json_dict['GEWICHT_0.3'],
            gewicht_1_2=json_dict['GEWICHT_1.2'],
            totaal=json_dict['TOTAAL'],

            jaar=year,
            peildatum=peildatum,
        )
        obj.vestiging_id = brin6 if brin6 in brin6s else None
        return obj


class LeerlingenNaarGewicht(models.Model):
    """Shadow relevant part of Leerling naar gewicht dataset of DUO."""
    # TODO: base links on the following (or build a BRIN 6 code)
    class Meta:
        unique_together = ('brin', 'vestigingsnummer', 'jaar')

    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    # relevant (subset) of properties
    # TODO: consider DecimalField
    gewicht_0 = models.FloatField()
    gewicht_0_3 = models.FloatField()
    gewicht_1_2 = models.FloatField()
    totaal = models.FloatField()

    # TODO: add peildatum (also jaar seperately)
    jaar = models.IntegerField()
    peildatum = models.DateField()

    objects = LeerlingenNaarGewichtManager()
    vestiging = models.ForeignKey(
        Vestiging, related_name='leerlingen_naar_gewicht', null=True)


_SCHOOLADVIEZEN_CSV_COLUMNS = collections.OrderedDict([
    ('PEILDATUM_LEERLINGEN', str),
    ('PEILDATUM_ADVIEZEN', str),  # old
    ('PRIKDATUM_ADVIEZEN', str),  # recent
    ('BRIN_NUMMER', str),
    ('VESTIGINGSNUMMER', int),
    ('INSTELLINGSNAAM_VESTIGING', str),
    ('POSTCODE_VESTIGING', str),
    ('PLAATSNAAM', str),
    ('GEMEENTENUMMER', int),
    ('GEMEENTENAAM', str),
    ('PROVINCIE', str),
    ('SOORT_PO', str),
    ('DENOMINATIE_VESTIGING', str),
    ('BEVOEGD_GEZAG_NUMMER', int),

    ('VSO', int),
    ('PRO', int),
    ('VMBO_BL', int),
    ('VMBO_BL_KL', int),
    ('VMBO_KL', int),
    ('VMBO_KL_GT', int),
    ('VMBO_GT', int),
    ('VMBO_GT_HAVO', int),
    ('HAVO', int),
    ('HAVO_VWO', int),
    ('VWO', int),
    ('ADVIES_NIET_MOGELIJK', int),
    ('TOTAAL_ADVIES', int),
])


class SchoolAdviezenManager(models.Manager):
    def _from_duo_csv(self, uri, year, brin6s):
        df = pandas.read_csv(
            uri,
            delimiter=';',
            dtype=_SCHOOLADVIEZEN_CSV_COLUMNS,
            encoding='cp1252'  # probable, not sure ... (at least not UTF8)
        )
        mask = df['GEMEENTENUMMER'] == 363  # only Amsterdam is relevant

        # Deal with rename of school types between 2013 and 2014:
        RENAMES = dict([
            ('VMBO_B', 'VMBO_BL'),
            ('VMBO_B_K', 'VMBO_BL_KL'),
            ('VMBO_K', 'VMBO_KL'),
            ('VMBO_K_GT', 'VMBO_KL_GT'),
            ('PRIKDATUM_ADVIEZEN', 'PEILDATUM_ADVIEZEN'),
        ])

        for column_name in df.columns:
            if column_name in RENAMES:
                df[RENAMES[column_name]] = df[column_name]

        # Cretae model instances and save them to database:
        instances = []
        for i, row in df[mask].iterrows():
            brin6 = row['BRIN_NUMMER'] + '{:02d}'.format(int(row['VESTIGINGSNUMMER']))
            peildatum_adviezen =  datetime.strptime(
                str(row['PEILDATUM_ADVIEZEN']), '%Y%m%d')
            peildatum_leerlingen = datetime.strptime(
                row['PEILDATUM_LEERLINGEN'], '%Y%m%d')

            obj = SchoolAdviezen(
                brin=row['BRIN_NUMMER'],
                vestigingsnummer=row['VESTIGINGSNUMMER'],

                vmbo_bl=row['VMBO_BL'],
                vmbo_bl_kl=row['VMBO_BL_KL'],
                vmbo_gt=row['VMBO_GT'],
                vmbo_gt_havo=row['VMBO_GT_HAVO'],
                vmbo_kl=row['VMBO_KL'],
                vmbo_kl_gt=row['VMBO_KL_GT'],
                vso=row['VSO'],
                vwo=row['VWO'],

                # new fields:
                havo = row['HAVO'],
                havo_vwo = row['HAVO_VWO'],
                pro = row['PRO'],

                jaar=year,
                peildatum_adviezen=peildatum_adviezen,
                peildatum_leerlingen=peildatum_leerlingen,
            )
            obj.vestiging_id = brin6 if brin6 in brin6s else None
            instances.append(obj)

        self.bulk_create(instances)


class SchoolAdviezen(models.Model):
    """Shadow relevant parst of School Adviezen dataset of DUO."""
    # TODO: base links on the following (or build a BRIN 6 code)
    class Meta:
        unique_together = ('brin', 'vestigingsnummer', 'jaar')

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

    # new:
    havo = models.IntegerField()
    havo_vwo = models.IntegerField()
    pro = models.IntegerField()

    jaar = models.IntegerField()
    # Recent data sets do not have the peildatum_adviezen (allow null)
    peildatum_adviezen = models.DateField(null=True)
    peildatum_leerlingen = models.DateField()

    # TODO: ga na wat 'PRO' betekend; school advies?
    objects = SchoolAdviezenManager()
    vestiging = models.ForeignKey(
        Vestiging, related_name='school_adviezen', null=True)


class CitoScoresManager(models.Manager, DUOAPIManagerMixin):
    def _from_duo_api_json_entry(self, json_dict, year, brin6s):
        brin6 = brin=json_dict['BRIN_NUMMER'] + \
            '{:02d}'.format(int(json_dict['VESTIGINGSNUMMER']))

        # Usage of case is not consistent over the years (in the data).
        upper = {key.upper(): key for key in json_dict}

        leerjaar8 = json_dict[upper['LEERJAAR_8']]
        raw = json_dict[upper['CET_GEM']].strip()

        # CITO scores can be missing
        cet_gem = raw.replace(',', '.') if raw else None

        obj = CitoScores(
            brin=json_dict['BRIN_NUMMER'],
            vestigingsnummer=json_dict['VESTIGINGSNUMMER'],
            cet_gem=cet_gem,
            leerjaar_8=leerjaar8,
            jaar=year,
        )
        obj.vestiging_id = brin6 if brin6 in brin6s else None
        return obj


class CitoScores(models.Model):
    """Shadow relevant parst of CITO Scores dataset of DUO."""
    # TODO: base links on the following (or build a BRIN 6 code)
    class Meta:
        unique_together = ('brin', 'vestigingsnummer', 'jaar')

    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    # relevant:
    # TODO: talk to experts about meaning of fields in DUO data
    # TODO: peildatum  / prikdatum
    cet_gem = models.FloatField(null=True)
    leerjaar_8 = models.IntegerField(null=True)

    jaar = models.IntegerField()
    objects = CitoScoresManager()
    vestiging = models.ForeignKey(
        Vestiging, related_name='cito_scores', null=True)


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

    jaar = models.IntegerField()


# -- datasets from onderwijs --

class SchoolWisselaarsManager(models.Manager):
    def _from_excel_file(self, file_name, brin6s):
        """
        Load Excel file of "schoolwisselaars", save to db.
        """
        # Load the Excel workbook, convert to Pandas DataFrame
        ws = load_workbook(file_name)['schoolwisseling in 2016 perc']
        data = ws.values
        columns = next(data)
        df = DataFrame(data, columns)

        # Report duplicated BRIN 6 codes:
        mask = df.duplicated(subset=['brin6'])
        duplicated_brin6s = set(df[mask]['brin6'])
        for brin6 in duplicated_brin6s:
            # TODO: proper logging
            print('Gedupliceerde BRIN6 {} wordt overgeslagen'.format(brin6))
            for i, row in df[df['brin6'] == brin6]:
                print('  {}: {}'.format(row['brin6'], row['schoolnaam']))

        instances = []
        for i, row in df.iterrows():
            if row['brin6'] in duplicated_brin6s:
                continue  # Skip records with duplicated BRIN 6 codes

            brin = row['brin6'][:4]
            vestigingsnummer = int(row['brin6'][4:])

            obj = SchoolWisselaars(
                brin=brin,
                vestigingsnummer=vestigingsnummer,
                naam=row['schoolnaam'],  # potential duplicate of Vestiging naam
                wisseling_uit=row['wisseling_uit'],
                wisseling_in=row['wisseling_in']
            )
            obj.vestiging_id = brin6 if brin6 in brin6s else None
            instances.append(obj)

        self.bulk_create(instances)

class SchoolWisselaars(models.Model):
    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    naam = models.CharField(max_length=255)
    wisseling_uit = models.FloatField()
    wisseling_in = models.FloatField()

    vestiging = models.ForeignKey(
        Vestiging, related_name='schoolwisselaars', null=True)
