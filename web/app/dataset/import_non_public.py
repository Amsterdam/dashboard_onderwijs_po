import os
import logging
# import objectstore

from .models import Subsidie
from .models import SchoolWisselaars

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# check local cache for needed files, then go to the object store
_CACHE_DIR = '/data/'

_SCHOOLWISSELAARS = {
    2015: '/levering_20171122/schoolwisselaars_PO 2015.xlsx',
}

_SUBSIDIES = {
    2017: '/levering_20171122/subsidies_22-11-2017.xlsx',
}

_VVE_LEERLINGEN = {
    2016: '/levering_20171122/VVE leerlingen 2016.xlsx',
}

_OBJECT_STORE_SETTINGS = {
    'VERSION': '2.0',
    'AUTHURL': 'https://identity.stack.cloudvps.com/v2.0',
    'TENANT_NAME': 'BGE000081_Onderwijs_storage',
    'TENANT_ID': '4e1bd5ced4064ddeb2acff5bba874707',
    'USER': 'onderwijs',
    'PASSWORD': os.getenv('ONDERWIJS_OBJECTSTORE_PASSWORD'),
    'REGION_NAME': 'NL',
}


def get_schoolwisselaars(year, brin6s):
    if year not in _SCHOOLWISSELAARS:
        return

    _path, _file = os.path.split(_SCHOOLWISSELAARS[year])
    if _file not in os.listdir(_CACHE_DIR):
        print('Need to grab file from objectstore')
        raise NotImplementedError('object store support TBD')

    file_name = os.path.join(_CACHE_DIR, _file)
    SchoolWisselaars.objects._from_excel_file(file_name, year, brin6s)


def get_subsidies(year, brin6s):
    if year not in _SUBSIDIES:
        return

    _path, _file = os.path.split(_SUBSIDIES[year])
    if _file not in os.listdir(_CACHE_DIR):
        print('Need to grab file from objectstore')
        raise NotImplementedError('object store support TBD')

    file_name = os.path.join(_CACHE_DIR, _file)
    Subsidie.objects._from_excel(file_name, year, brin6s)

