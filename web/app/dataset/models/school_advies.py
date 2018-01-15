"""
Modellen voor School types en adviezen uit DUO data.
"""
import pandas
from django.db import models
from django.core.exceptions import ValidationError

from .vestiging import Vestiging

# School types that we save to the database, anything else will fail.
SCHOOL_TYPES = [
    'VMBO_BL',
    'VMBO_BL_KL',
    'VMBO_GT',
    'VMBO_GT_HAVO',
    'VMBO_KL',
    'VMBO_KL_GT',
    'VSO',
    'VWO',
    'HAVO',
    'HAVO_VWO',
    'PRO'
]

# Mapping from school types that we do not store to those we do:
# (There was a slight rename in the data between 2013 and 2014).
SCHOOL_TYPE_MAPPING = dict([
    ('VMBO_B', 'VMBO_BL'),
    ('VMBO_B_K', 'VMBO_BL_KL'),
    ('VMBO_K', 'VMBO_KL'),
    ('VMBO_K_GT', 'VMBO_KL_GT'),
    ('PRIKDATUM_ADVIEZEN', 'PEILDATUM_ADVIEZEN'),
])

# Columns in data files
_SCHOOLADVIEZEN_CSV_COLUMNS = dict([
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


class SchoolTypeManager(models.Manager):
    def create_known(self):
        '''
        Initialize the SchoolType table, no need to manually create more entries.
        '''
        instances = []
        for name in SCHOOL_TYPES:
            instances.append(SchoolType(name=name))
        self.bulk_create(instances)


class SchoolType(models.Model):
    name = models.CharField(max_length=16, primary_key=True)

    objects = SchoolTypeManager()

    def clean(self):
        if self.name not in SCHOOL_TYPES:
            msg = '{} not a valid schooltype'.format(self.name)
            raise ValidationError(msg)


class SchoolAdviesManager(models.Manager):
    def import_csv(self, uri, year, brin6s):
        """
        Retrieve CSV data from uri create SchoolAdvies entries.
        """
        # TODO: Check encoding='cp1252' with source.
        df = pandas.read_csv(
            uri,
            delimiter=';',
            dtype=_SCHOOLADVIEZEN_CSV_COLUMNS,
            encoding='cp1252'
        )
        mask = df['GEMEENTENUMMER'] == 363  # only Amsterdam is relevant

        # Deal with rename of school types between 2013 and 2014:
        for column_name in df.columns:
            if column_name in SCHOOL_TYPE_MAPPING:
                df[SCHOOL_TYPE_MAPPING[column_name]] = df[column_name]

        # Cretae model instances and save them to database:
        instances = []
        for i, row in df[mask].iterrows():
            brin6 = row['BRIN_NUMMER'] + '{:02d}'.format(int(row['VESTIGINGSNUMMER']))
            # TODO: check whether this information is needed
            # peildatum_adviezen =  datetime.strptime(
            #     str(row['PEILDATUM_ADVIEZEN']), '%Y%m%d')
            # peildatum_leerlingen = datetime.strptime(
            #     row['PEILDATUM_LEERLINGEN'], '%Y%m%d')

            # Make an SchoolAdvies entry for each type of school.
            for school_type in SCHOOL_TYPES:
                obj = SchoolAdvies(
                    brin=row['BRIN_NUMMER'],
                    vestigingsnummer=row['VESTIGINGSNUMMER'],

                    advies_id=school_type,
                    totaal=row[school_type],
                    jaar=year,
                )
                obj.vestiging_id = brin6 if brin6 in brin6s else None
                instances.append(obj)

        self.bulk_create(instances)


class SchoolAdvies(models.Model):
    class Meta:
        unique_together = ('brin', 'vestigingsnummer', 'jaar', 'advies')

    # for internal bookkeeping (keep track of missing vestigingen)
    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    # to expose to outside
    advies = models.ForeignKey(
        SchoolType, on_delete=models.CASCADE, related_name='schooladviezen')
    totaal = models.IntegerField()
    jaar = models.IntegerField()
    vestiging = models.ForeignKey(
        Vestiging, on_delete=models.SET_NULL,
        null=True,
    )

    objects = SchoolAdviesManager()
