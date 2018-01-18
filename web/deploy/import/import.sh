#!/bin/sh

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose -p onderwijs -f ${DIR}/docker-compose.yml $*
}

trap 'dc kill ; dc rm -f' EXIT

# For database backups:
rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

echo "For debugging list volumes"
dc down	-v
docker volume ls

echo "Building images"
dc build

echo "Bringing up and waiting for database"
dc up -d database
dc run importer /deploy/docker-wait.sh

echo "Downloading raw datafiles from object store"
dc run --rm importer ls /data
dc run --rm importer python manage.py download_data
dc run --rm importer python manage.py migrate
dc run --rm importer python manage.py run_import
dc run --rm importer python manage.py import_non_public
dc run --rm importer python manage.py calc_aggregates

echo "Running backups"
# these are still "old style"

dc exec -T database backup-db.sh onderwijs
echo "Done"
