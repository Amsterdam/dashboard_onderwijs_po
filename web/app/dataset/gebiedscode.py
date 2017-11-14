"""
Given an adress from schoolwijzer, query BAG search for "gebiedscode".
"""
# TODO: make more general, currently only implemented for buurt
import json
import logging

import requests

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


logging.getLogger("chardet").setLevel(logging.WARNING)


def find_gebiedscode(lat, lon, adres):
    """
    Find buurt_code for each vestiging (or vestiging adres).
    """
    buurt_codes = [_adres_to_buurt_code(adres)]
    buurt_codes.append(_lat_lon_to_buurt_code(lat, lon))

    if buurt_codes[0] is None and buurt_codes[1] is None:
        print('!!! NO MATCH FOR :', adres)
    if buurt_codes[0] and buurt_codes[1] and buurt_codes[0] != buurt_codes[1]:
        print('!!! TWO MATCHES  :', adres)

    # Choose best code (based on addres, fallback is lat/lon):
    buurt_code = buurt_codes[0] if buurt_codes[0] else buurt_codes[1]

    return buurt_code


def _adres_to_buurt_code(adres):
    """
    Search BAG with adres from schoolwijzer.nl to determine the buurt code.
    """
    BAG_SEARCH_URL = 'https://api.data.amsterdam.nl/atlas/search/adres/'
    parameters = {'q': adres}

    result = requests.get(BAG_SEARCH_URL, parameters)
    assert result.status_code == 200
    data = json.loads(result.text)

    if data['count']:
        # For now use first match.
        uri = data['results'][0]['_links']['self']['href']
        buurt_code = _nummer_aanduiding_to_buurt_code(uri)
    else:
        buurt_code = None

    return buurt_code


def _nummer_aanduiding_to_buurt_code(uri):
    """
    Grab buurt code from nummer aanduiding instance endpoint.
    """
    result = requests.get(uri)
    assert result.status_code == 200

    data = json.loads(result.text)
    if 'detail' in data:
        buurt_code = None
    else:
        buurt_uri = data['buurt']['_links']['self']['href']
        buurt_code = _buurt_to_code(buurt_uri)

    return buurt_code


def _lat_lon_to_buurt_code(lat, lon):
    """
    Query Geo search API and BBGA for buurt combinatie code.
    """
    GEOSEARCH_URL = 'https://api.data.amsterdam.nl/geosearch/search/'
    parameters = {
        'item': 'buurt',
        'lat': lat,
        'lon': lon
    }

    result = requests.get(GEOSEARCH_URL, parameters)
    assert result.status_code == 200

    data = json.loads(result.text)

    # check GeoJSON data for features
    if data['features']:
        # For now use first match.
        uri = data['features'][0]['properties']['uri']
        buurt_code = _buurt_to_code(uri)
    else:
        buurt_code = None

    return buurt_code


def _buurt_to_code(uri):
    """
    Given buurt URI, return "volledige_code".
    """
    result = requests.get(uri)
    assert result.status_code == 200

    data = json.loads(result.text)
    if 'detail' in result:
        return None
    else:
        return data['volledige_code']
