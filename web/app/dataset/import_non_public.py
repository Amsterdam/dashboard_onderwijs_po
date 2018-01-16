import os
import logging
# import objectstore

from .models.subsidie import subsidie_import_helper
from .models import SchoolWisselaars

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# check local cache for needed files, then go to the object store
_CACHE_DIR = '/data/'

# schooljaar 2016/2017 is ook beschikbaar
_SCHOOLWISSELAARS = {
    2016: '/levering_20171122/schoolwisselaars_PO 2015.xlsx',
}

# waarschijnlijk alleen 2017 (niet ouder)
_SUBSIDIES = {
    2017: '/levering_20171122/subsidies_22-11-2017.xlsx',
}

# tbd
_VVE_LEERLINGEN = {
    2016: '/levering_20171122/VVE leerlingen 2016.xlsx',
}

_OBJECT_STORE_SETTINGS = {
    'VERSION': '2.0',
    'AUTHURL': 'https://identity.stack.cloudvps.com/v2.0',
    'TENANT_ID': 'c9089d4a49934890baf2569cdc587571',
    'USER': 'onderwijs',
    'PASSWORD': os.getenv('ONDERWIJS_OBJECTSTORE_PASSWORD'),
    'REGION_NAME': 'NL',
}


def full_split(path, make_relative):
    """
    Return list of path elements. If make_relative then remove / (root).
    """
    reversed_chunks = []

    start, end = os.path.split(path)
    while end != '':
        reversed_chunks.append(end)
        start, end = os.path.split(start)

    if start != '' and (start != '/' or (not make_relative)):
        reversed_chunks.append(start)

    return list(reversed(reversed_chunks))


def get_schoolwisselaars(year, brin6s):
    if year not in _SCHOOLWISSELAARS:
        return

    file_name = os.path.join(
        _CACHE_DIR,
        *full_split(_SCHOOLWISSELAARS[year], make_relative=True)
    )

    if not os.path.exists(file_name):
        raise Exception('Data file not present: {}'.format(file_name))
    logger.debug('Accessing: {}'.format(file_name))

    SchoolWisselaars.objects._from_excel_file(file_name, year, brin6s)


def get_subsidies(year, brin6s):
    if year not in _SUBSIDIES:
        return

    file_name = os.path.join(
        _CACHE_DIR,
        *full_split(_SUBSIDIES[year], make_relative=True)
    )

    if not os.path.exists(file_name):
        raise Exception('Data file not present: {}'.format(file_name))
    logger.debug('Accessing: {}'.format(file_name))

    subsidie_import_helper(file_name, year, brin6s)
