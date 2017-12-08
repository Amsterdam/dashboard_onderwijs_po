"""
Import code for DUO data sets.
"""
# flake8: noqa

# TODO items:
# * consider using DRF serializers for creating new Model instances
# * investigate whether JSON-LD can be used directly to validate received data
# * remove debug prints, replace with logging where needed

import json
import logging

import requests
import pandas
from jsonschema import validate
from dataset.models import LeerlingNaarGewicht
from dataset.models import SchoolAdvies
from dataset.models import CitoScores

from dataset.models import Vestiging
from django.conf import settings


LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

_BASE_API_URL = 'https://api.duo.nl/v0/datasets/'

_CITO_SCORES = {
    2014: 'https://api.duo.nl/v0/datasets/05.-gemiddelde-eindscores-bo-sbo-2014-2015/search',
    2015: 'https://api.duo.nl/v0/datasets/05.-gemiddelde-eindscores-bo-sbo-2015-2016/search'
}

_LEERLING_NAAR_GEWICHT_CSV = {
    2014: 'https://duo.nl/open_onderwijsdata/images/02.leerlingen-bo-swv-vestiging%2C-gewicht%2C-impulsgebied%2C-schoolgewicht-2014-2015.csv',
    2015: 'https://duo.nl/open_onderwijsdata/images/02.-leerlingen-bo-swv-vestiging%2C-gewicht%2C-impulsgebied%2C-schoolgewicht-2015-2016.csv',
    2016: 'https://duo.nl/open_onderwijsdata/images/02.leerlingen-bo-swv-vestiging%2C-gewicht%2C-impulsgebied%2C-schoolgewicht-2016-2017.csv',
}

_CSV_SCHOOL_ADVIEZEN = {
    2011: 'https://duo.nl/open_onderwijsdata/images/04.-leerlingen-bo-sbo-schooladviezen-2011-2012.csv',
    2012: 'https://duo.nl/open_onderwijsdata/images/04.-leerlingen-bo-sbo-schooladviezen-2012-2013.csv',
    2013: 'https://duo.nl/open_onderwijsdata/images/04.-leerlingen-bo-sbo-schooladviezen-2013-2014.csv',
    2014: 'https://duo.nl/open_onderwijsdata/images/04.-schooladviezen-2014-2015.csv',  # different columns as above earlier data
    2015: 'https://duo.nl/open_onderwijsdata/images/04.-schooladviezen-2015-2016.csv',
}


def _download_json(dataset, year):
    API_URL = dataset[year]
    PARAMETERS = {'uni_gemeentenaam': 'amsterdam'}

    # Retrieve the JSON encoded data:
    result = requests.get(API_URL, PARAMETERS)
    logger.info('Retrieved: %s', result.url)
    assert result.status_code == 200

    return json.loads(result.text)


def get_cito_scores(year, brin6s):
    try:
        data = _download_json(_CITO_SCORES, year)
    except KeyError:
        pass
    else:
        CitoScores.objects.from_duo_api_json(data, year, brin6s)


def get_school_advies(year, brin6s):
    try:
        url = _CSV_SCHOOL_ADVIEZEN[year]
    except KeyError:
        pass
    else:
        SchoolAdvies.objects.import_csv(url, year, brin6s)


def get_leerling_naar_gewicht(year, brin6s):
    try:
        url = _LEERLING_NAAR_GEWICHT_CSV[year]
    except KeyError:
        pass
    else:
        LeerlingNaarGewicht.objects.import_csv(url, year, brin6s)

