"""
Given an adress from schoolwijzer, query BAG search for "gebiedscode".
"""
# TODO: make more general, currently only implemented for buurt
import json
import logging

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

logging.getLogger("chardet").setLevel(logging.WARNING)

BUURT = 0
GEBIEDSGERICHT_WERKEN = 1


def find_gebiedscode(lat, lon, adres, _type):
    """
    Find buurt_code or gebiedsgerichtwerken code given lat/lon and adress.
    """
    with _get_session_with_retries() as s:
        buurt_codes = [_adres_to_gebiedscode(s, adres, _type=_type)]
        buurt_codes.append(_lat_lon_to_gebiedscode(s, lat, lon, _type=_type))

    if buurt_codes[0] is None and buurt_codes[1] is None:
        raise NoAreaMatch()
    if buurt_codes[0] and buurt_codes[1] and buurt_codes[0] != buurt_codes[1]:
        logger.info('Voor adres {} en (lat={}, lon={}) twee gebieden {}.'.format(
            adres, lat, lon, buurt_codes
        ))

    # Choose best code (based on addres, fallback is lat/lon):
    buurt_code = buurt_codes[0] if buurt_codes[0] else buurt_codes[1]

    return buurt_code


def _get_session_with_retries():
    """
    Get a requests Session that will retry some set number of times.
    """
    session = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=True
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    return session


def NoAreaMatch(Exception):
    pass


def _adres_to_gebiedscode(session, adres, _type):
    """
    Search BAG adresses to determine the buurt or gebiedsgerichtwerken code.
    """
    BAG_SEARCH_URL = 'https://api.data.amsterdam.nl/atlas/search/adres/'
    parameters = {'q': adres}

    result = session.get(BAG_SEARCH_URL, params=parameters)

    if result.status_code != 200:
        logger.info('Got status code {} while accessing: {}'.format(
            result.status_code, result.url))
        return None

    data = result.json()
    # For now use first match.
    if data['count']:
        uri = data['results'][0]['_links']['self']['href']
        gebiedscode = _nummer_aanduiding_to_gebiedscode(session, uri, _type)
    else:
        gebiedscode = None

    return gebiedscode


def _nummer_aanduiding_to_gebiedscode(session, uri, _type):
    """
    buurt or gebiedsgerichtwerken code from nummeraanduiding instance endpoint.
    """
    result = session.get(uri)

    if result.status_code != 200:
        logger.info('Got status code {} while accessing: {}'.format(
            result.status_code, result.url))
        return None

    data = result.json()
    if 'detail' in data:
        gebiedscode = None
    else:
        if _type == BUURT:
            buurt_uri = data['buurt']['_links']['self']['href']
            gebiedscode = _buurt_to_code(buurt_uri)
        elif _type == GEBIEDSGERICHT_WERKEN:
            gebiedscode = data['_gebiedsgerichtwerken']['code']
        else:
            raise ValueError('Unknown area type %s' % _type)

    return gebiedscode


def _lat_lon_to_gebiedscode(session, lat, lon, _type):
    """
    Query Geo search API and BBGA for buurt or gebiedsgerichtwerken code.
    """
    if _type not in [BUURT, GEBIEDSGERICHT_WERKEN]:
        raise ValueError('Unknown area type %s' % _type)

    GEOSEARCH_URL = 'https://api.data.amsterdam.nl/geosearch/search/'
    parameters = {
        'item': ['buurt', 'gebiedsgerichtwerken'][_type],
        'lat': lat,
        'lon': lon
    }

    result = session.get(GEOSEARCH_URL, params=parameters)
    try:
        assert result.status_code == 200
    except AssertionError:
        logger.info('Got status code {} while accessing: {}'.format(
            result.status_code, result.url))
        raise

    data = json.loads(result.text)

    # For now use first match.
    if data['features']:
        if _type == BUURT:
            uri = data['features'][0]['properties']['uri']
            gebiedscode = _buurt_to_code(uri)
        elif _type == GEBIEDSGERICHT_WERKEN:
            gebiedscode = data['features'][0]['properties']['id']
    else:
        gebiedscode = None

    return gebiedscode


def _buurt_to_code(session, uri):
    """
    Given buurt URI, return "volledige_code".
    """
    result = session.get(uri)
    if result.status_code != 200:
        logger.info('Got status code {} while accessing: {}'.format(
            result.status_code, result.url))
        return None

    data = result.json()
    if 'detail' in result:
        return None
    else:
        return data['volledige_code']
