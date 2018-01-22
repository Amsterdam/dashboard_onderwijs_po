# Dashboard Primair Onderwijs
## Context
For primary education in Amsterdam, this project aims to provide a simple
dashboard that summarizes basic data about primary schools and their
catchment area.

## Requirements
* A Docker installation with `docker-compose`.
* Git
* Optionally (priviliged data, available only within the Amsterdam municipality).


## Running the service locally
The service is fully containerized and for running it locally and developing
it further a `docker-compose` setup is provided. By running the following
commands you will get a locally running version of the webservice at HTTP port
8000.

Get the storage password from the password manager and set the corresponding environment variable:

    export ONDERWIJS_OBJECTSTORE_PASSWORD=...

```bash
docker-compose build
docker-compose up -d database
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py run_import
docker-compose up web
```

You can no point your browser to `http://127.0.0.1:8000/onderwijs/` to access
the Onderwijs (Education) API endpoints. Note, some of the data requires
special priviliges to import, the standard `run_import` command will therefore
not download this data. If you have these priviliges (only for a subset of
Amsterdam municipal employees) you can mount the required data under /data in
the container. (Latter is subject to change, and will be futher automated.)
If the priviliged data is available running the following command will add that
data to the service:

```bash
docker-compose run --rm web python manage.py download_data
docker-compose run --rm web python manage.py import_non_public
```

The dashboard pages are available under:
`http://127.0.0.1:8000/onderwijs/dash/vestiging/` (Subject to change during
further development).

## Local development
The service is setup to run locally using bind mounts to the host system
that has the Git repository. The `/web/app` and `/web/deploy` directories
use a bind mount, and edited source will be available immediately in the
running Docker container. The `docker-compose.yml` file in the project
root is set up to use the Django development server, which will reload
immediately (so changes to the Django/Python app sources are reflected in
the running app immediately).

For development you can follow the same instructions as those for running
the service locally (documented in the previous section).


## Running the tests
While the test suite is still a work in progress, it can be run using the
following command:

```
docker-compose -f ./web/deploy/test/docker-compose.yml run tests
```

Note that for now, the import process test is using the real data sources
and imports the whole dataset (so the tests will be a bit slow).


## About the datasources
* https://schoolwijzer.amsterdam.nl/nl/
* https://duo.nl/open_onderwijsdata/databestanden/index.jsp
* https://api.data.amsterdam.nl/bbga/
* https://api.data.amsterdam.nl/bag/
* Gemeente Amsterdam, Cluster sociaal; Onderwijs, Jeugd en Zorg.
