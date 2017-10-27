# flake8: noqa
import json

import requests
from jsonschema import validate
from dataset.models import Vestiging, Adres

# hit schoolwijzer URL, download the vestigingen


def _handle_vestiging_adres(json_dict):
    adres = Adres(**json_dict)
    adres.save()
    return adres


def _handle_vestiging(json_dict):
    adres = _handle_vestiging_adres(json_dict['adres'])

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
        vestigingsnummer=json_dict['vestigingsnummer']
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

    Vestiging.objects.bulk_create(instances)
    print('Number of vestigingen', len(data['results']))
    print('  Number of vestigingen in DB', Vestiging.objects.count())

