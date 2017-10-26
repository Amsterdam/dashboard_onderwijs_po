"""
Import code for DUO data sets.
"""
# TODO items:
# * consider using DRF serializers for creating new Model instances
# * investigate whether JSON-LD can be used directly to validate received data

import json

import requests
import pandas
from jsonschema import validate
from dataset.models import LeerlingenNaarGewicht
from dataset.models import SchoolAdviezen
from dataset.models import CitoScores


_BASE_API_URL = 'https://api.duo.nl/v0/datasets/'


# -- leerlingen naar gewicht ---

def _handle_leerlingen_naar_gewicht(json_dict):
    out = LeerlingenNaarGewicht(
        brin=json_dict['BRIN_NUMMER'],
        vestigingsnummer=json_dict['VESTIGINGSNUMMER'],

        gewicht_0=json_dict['GEWICHT_0'],
        gewicht_0_3=json_dict['GEWICHT_0.3'],
        gewicht_1_2=json_dict['GEWICHT_1.2'],
        # TODO: add peildatum, jaar
    )
    out.full_clean()
    return out


def get_leerlingen_naar_gewicht():
    DATA_SET = '02.leerlingen-bo-swv-vestiging%2C-gewicht%2C-impulsgebied%2C-schoolgewicht-2014-2015/search'
    PARAMETERS = {'uni_gemeentenaam': 'amsterdam'}
    API_URL = requests.compat.urljoin(_BASE_API_URL, DATA_SET)

    result = requests.get(API_URL, PARAMETERS)
    assert result.status_code == 200

    data = json.loads(result.text)
    for entry in data['results']:
        _handle_leerlingen_naar_gewicht(entry)
    print('Number of results leerlingen naar gewicht', len(data['results']))


# -- school adviezen --

def _handle_school_adviezen(json_dict):
    out = SchoolAdviezen(
        brin=json_dict['BRIN_NUMMER'],
        vestigingsnummer=json_dict['VESTIGINGSNUMMER'],

        vmbo_bl=json_dict['VMBO_BL'],
        vmbo_bl_kl=json_dict['VMBO_BL_KL'],
        vmbo_gt=json_dict['VMBO_GT'],
        vmbo_gt_havo=json_dict['VMBO_GT_HAVO'],
        vmbo_kl=json_dict['VMBO_KL'],
        vmbo_kl_gt=json_dict['VMBO_KL_GT'],
        vso=json_dict['VSO'],
        vwo=json_dict['VWO'],
    )
    out.full_clean()
    return out


def get_school_adviezen():
    DATA_SET = '04.-leerlingen-bo-sbo-schooladviezen-2013-2014/search'
    PARAMETERS = {'uni_gemeentenaam': 'amsterdam'}
    API_URL = requests.compat.urljoin(_BASE_API_URL, DATA_SET)

    result = requests.get(API_URL, PARAMETERS)
    assert result.status_code == 200

    data = json.loads(result.text)
    for entry in data['results']:
        tmp = _handle_school_adviezen(entry)
    print('Number of School Adviezen entries:', len(data['results']))


# -- Cito scores --

def _handle_cito_scores(json_dict):
    cito_scores = CitoScores(
        brin=json_dict['BRIN_NUMMER'],
        vestigingsnummer=json_dict['VESTIGINGSNUMMER'],

        cet_gem=json_dict['cet_gem'].replace(',', '.'),
        leerjaar_8=json_dict['Leerjaar_8']
    )
    cito_scores.full_clean()  # needed to check inputs, when not saving
    return cito_scores


def get_cito_scores():
    DATA_SET = '05.-gemiddelde-eindscores-bo-sbo-2014-2015/search'
    PARAMETERS = {'uni_gemeentenaam': 'amsterdam'}
    API_URL = requests.compat.urljoin(_BASE_API_URL, DATA_SET)

    result = requests.get(API_URL, PARAMETERS)
    assert result.status_code == 200

    data = json.loads(result.text)
    for entry in data['results']:
        tmp = _handle_cito_scores(entry)
    print('Number of CITO scores entries:', len(data['results']))


# -- leerling leraar ratio --


def get_leerling_leraar_ratios():
    DATA_SET_URL = 'https://duo.nl/open_onderwijsdata/images/01.-po-personen-owtype-bestuur-brin-functie.csv'

    # Style: process full datafile in memory, than drop clean data in database.
    # TODO: seems to be availabel per BRIN, not vestiging -> check

    df = pandas.read_csv(DATA_SET_URL, delimiter=';', decimal='.')
    # filter by BRIN nummers
    brin_nummers = []  # select from Vestiging model TODO
    relevant = df.loc[df['BRIN NUMMER'].isin(brin_nummers)]





