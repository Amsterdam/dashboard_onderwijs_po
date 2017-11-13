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
from dataset.models import LeerlingenNaarGewicht
from dataset.models import SchoolAdviezen
from dataset.models import CitoScores

from dataset.models import Vestiging
from django.conf import settings


LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

_BASE_API_URL = 'https://api.duo.nl/v0/datasets/'

_LEERLINGEN_NAAR_GEWICHT = {
    2014: 'https://api.duo.nl/v0/datasets/02.leerlingen-bo-swv-vestiging%2C-gewicht%2C-impulsgebied%2C-schoolgewicht-2014-2015/search',
    2015: 'https://api.duo.nl/v0/datasets/02.-leerlingen-bo-swv-vestiging%2C-gewicht%2C-impulsgebied%2C-schoolgewicht-2015-2016/search',
    2016: 'https://api.duo.nl/v0/datasets/02.leerlingen-bo-swv-vestiging%2C-gewicht%2C-impulsgebied%2C-schoolgewicht-2016-2017/search'
}

_SCHOOL_ADVIEZEN = {
    2011: 'https://api.duo.nl/v0/datasets/04.-leerlingen-bo-sbo-schooladviezen-2011-2012/search',
    2012: 'https://api.duo.nl/v0/datasets/04.-leerlingen-bo-sbo-schooladviezen-2012-2013/search',
    2013: 'https://api.duo.nl/v0/datasets/04.-leerlingen-bo-sbo-schooladviezen-2013-2014/search',
    2014: 'https://api.duo.nl/v0/datasets/04.-adviezen-2014-2015-inclusief-herziening/search',
    2015: 'https://api.duo.nl/v0/datasets/04.-adviezen-2015-2016-inclusief-herziening/search'
}

_CITO_SCORES = {
    2014: 'https://api.duo.nl/v0/datasets/05.-gemiddelde-eindscores-bo-sbo-2014-2015/search',
    2015: 'https://api.duo.nl/v0/datasets/05.-gemiddelde-eindscores-bo-sbo-2015-2016/search'
}


def _download_json(dataset, year):
    API_URL = dataset[year]
    PARAMETERS = {'uni_gemeentenaam': 'amsterdam'}

    # Retrieve the JSON encoded data:
    result = requests.get(API_URL, PARAMETERS)
    logger.info('Retrieved: %s', result.url)
    assert result.status_code == 200

    return json.loads(result.text)


def get_leerlingen_naar_gewicht(year, brin6s):
    try:
        data = _download_json(_LEERLINGEN_NAAR_GEWICHT, year)
    except KeyError:
        pass
    else:
        LeerlingenNaarGewicht.objects.from_duo_api_json(data, year, brin6s)


def get_school_adviezen(year, brin6s):
    try:
        data = _download_json(_SCHOOL_ADVIEZEN, year)
    except KeyError:
        pass
    else:
        SchoolAdviezen.objects.from_duo_api_json(data, year, brin6s)


def get_cito_scores(year, brin6s):
    try:
        data = _download_json(_CITO_SCORES, year)
    except KeyError:
        pass
    else:
        CitoScores.objects.from_duo_api_json(data, year, brin6s)

