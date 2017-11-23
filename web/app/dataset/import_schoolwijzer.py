# flake8: noqa
import json
import logging

import requests
from jsonschema import validate
from dataset.models import Vestiging, Adres
from dataset.gebiedscode import find_gebiedscode, GEBIEDSGERICHT_WERKEN


LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _handle_vestiging_adres(json_dict):
    adres = Adres(**json_dict)
    adres.save()
    return adres


def _handle_vestiging(json_dict):
    adres = _handle_vestiging_adres(json_dict['adres'])

    if json_dict['vestigingsnummer'] is None:
        print('Vestiging "{}" zonder vestigingsnummer wordt overgeslagen.'.format(
            json_dict['naam']
        ))
        print('Vestiging "{}" heeft BRIN nummer: {}'.format(
            json_dict['naam'], json_dict['brin']
        ))
        return

    brin6 = json_dict['brin'] + '{:02d}'.format(int(json_dict['vestigingsnummer']))

    gc = find_gebiedscode(
        lat=json_dict['coordinaten']['lat'],
        lon=json_dict['coordinaten']['lng'],
        adres=adres.adres,
        _type=GEBIEDSGERICHT_WERKEN
    )

    vestiging = Vestiging(
        adres=adres,
        brin=json_dict['brin'],
        lat=json_dict['coordinaten']['lat'],
        lon=json_dict['coordinaten']['lng'],
        grondslag=json_dict['grondslag'],
        heeft_voorschool=json_dict['heeft_voorschool'],
        _id=json_dict['id'],
        leerlingen=json_dict['leerlingen'],
        naam=json_dict['naam'],
        onderwijsconcept=json_dict['onderwijsconcept'],
        schoolwijzer_url=json_dict['schoolwijzer_url'],
        vestigingsnummer=json_dict['vestigingsnummer'],
        brin6=brin6,
        gebiedscode=gc
    )

    return vestiging


def get_vestigingen():
    API_URL = 'https://schoolwijzer.amsterdam.nl/nl/api/v1/lijst/po/'
    result = requests.get(API_URL)
    assert result.status_code == 200
    data = json.loads(result.text)

    # TODO: do the json-schema validation here

    instances = []
    for entry in data['results']:
        instances.append(_handle_vestiging(entry))

    Vestiging.objects.bulk_create([x for x in instances if x is not None])
    print('Number of vestigingen', len(data['results']))
    print('  Number of vestigingen in DB', Vestiging.objects.count())

