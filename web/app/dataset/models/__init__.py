# flake8: noqa
import logging

from .vestiging import Adres, Vestiging
from .leerling_naar_gewicht import LeerlingNaarGewicht
from .school_advies import SchoolType, SchoolAdvies
from .cito_scores import CitoScores
from .llratio import LeerlingLeraarRatio
from .school_wisselaars import SchoolWisselaars
from .subsidie import Subsidie, ToegewezenSubsidie

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def report_rows():
    """
    Log the number of entries for all models in this app.
    """
    _models = [
        Adres, Vestiging, LeerlingNaarGewicht, SchoolType, SchoolAdvies,
        CitoScores, LeerlingLeraarRatio, SchoolWisselaars, Subsidie,
        ToegewezenSubsidie
    ]

    logger.debug('Tellingen van database rijen:')
    for m in _models:
        msg = '  Telling {} rijen: {}'.format(m.__name__, m.objects.count())
        logger.debug(msg)
