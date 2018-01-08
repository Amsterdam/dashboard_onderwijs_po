import logging

from django.conf import settings
from django.db import connection
from django.http import HttpResponse

from dataset.models import Vestiging
from dataset.models import LeerlingNaarGewicht
from dataset.models import SchoolType, SchoolAdvies
from dataset.models import CitoScores
from dataset.models import LeerlingLeraarRatio


logger = logging.getLogger(__name__)


def health(request):
    """
    Basic health check view, returns 200 if services is running properly.
    """

    # We do not allow DEBUG mode in production environments.
    if settings.DEBUG:
        logger.exception("Debug mode not allowed in production")
        return HttpResponse(
            "Debug mode not allowed in production",
            content_type="text/plain", status=500)

    # Check database connection.
    try:
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            assert cursor.fetchone()
    except:  # noqa E722
        logger.exception("Database connectivity failed")
        return HttpResponse(
            "Database connectivity failed",
            content_type="text/plain", status=500)

    return HttpResponse(
        "Connectivity OK", content_type='text/plain', status=200)


def check_data(request):
    """
    Basic check for presence of data in the database.
    """

    # TODO: Add checks for priviliged data, once their handling is settled.
    if not Vestiging.objects.count():
        msg = 'There are no "Vestiging" entries.'
        status = 500
    elif not LeerlingNaarGewicht.objects.count():
        msg = 'There are no "Leerling naar Gewicht" entries.'
        status = 500
    elif not SchoolAdvies.objects.count():
        msg = 'There are no "School Advies" entries.'
        status = 500
    elif not SchoolType.objects.count():
        msg = 'There are no "School Type" entries.'
        status = 500
    elif not CitoScores.objects.count():
        msg = 'There are no "Cito Scores" entries.'
        status = 500
    elif not LeerlingLeraarRatio.objects.count():
        msg = 'There are no "Leerling Leraar Ratio" entries.'
        status = 500
    else:
        msg = 'Public data are available - basic database check passes. ' \
              'No guarantee about referential integrity.'
        status = 200

    return HttpResponse(
        msg, content_type='text/plain', status=status)
