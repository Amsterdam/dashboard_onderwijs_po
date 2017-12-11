import os

from onderwijs.settings_common import * # noqa F403
from onderwijs.settings_common import INSTALLED_APPS, DEBUG # noqa F401
from onderwijs.settings_databases import LocationKey,\
    get_docker_host,\
    get_database_key,\
    OVERRIDE_HOST_ENV_VAR,\
    OVERRIDE_PORT_ENV_VAR

INSTALLED_APPS += [
    'rest_framework_swagger',
    'health',  # health checks for deployment
    'dataset',  # import code
    'api',  # REST API code
    'web',
    'corsheaders',  # CORS headers for dashboard development purposes
]

ROOT_URLCONF = 'onderwijs.urls'


WSGI_APPLICATION = 'onderwijs.wsgi.application'

DATABASE_OPTIONS = {
    LocationKey.docker: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'onderwijs'),
        'USER': os.getenv('DATABASE_USER', 'onderwijs'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': 'database',
        'PORT': '5432'
    },
    LocationKey.local: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'onderwijs'),
        'USER': os.getenv('DATABASE_USER', 'onderwijs'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5412'
    },
    LocationKey.override: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'onderwijs'),
        'USER': os.getenv('DATABASE_USER', 'onderwijs'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432')
    },
}

DATABASES = {
    'default': DATABASE_OPTIONS[get_database_key()]
}

# Directory for raw test data:
TESTDATA_DIR = os.path.join(BASE_DIR, 'test_data') # noqa F405

# Settings for onderwijs dashboard imports
ONDERWIJS = {
    'YEARS': [
        2014,
        2015,
        2016
    ],
}
