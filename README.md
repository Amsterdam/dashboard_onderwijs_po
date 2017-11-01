# Dashboard Primair Onderwijs
## Requirements
* A Docker installation with `docker-compose`.


## Developing (in Docker container)
`docker-compose -f docker-compose-dev.yml up`

The `docker-compose-dev.yml` file is set up such that it will mount your
Python source in the running container. The `/app` and `/deploy`
directories in the running `web` container will be mapped to the `web/app/`
and `web/deploy` directories on your host system. That way you can edit the
source on your host system and the changes will be available immediately in
the running container. This is called a bind mount in Docker.
The `docker-compose-dev.yml` file furthermore uses the Django development
server because that server will reload automatically on a change in the
Python source code.


## Running tests
TBD
