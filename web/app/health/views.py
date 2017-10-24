import logging

from django.conf import settings
from django.db import connection
from django.http import HttpResponse

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
    # TODO: Implement when models are available, raise HTTP 500 on problems.
    return HttpResponse(
        "Database data OK", content_type='text/plain', status=200)
