# Jenkins workaround
FROM amsterdam/python

# Build one Docker container that servers both the Django application and
# the Vue.js based frontend. Hence the location of this Dockerfile, it needs
# access to source of both these services. We may split these out into their
# own containers and host them at different locations at a later date.

# Build JavaScript app
FROM node:8.1-alpine as builder
  ARG NODE_ENV=development
  WORKDIR /app
  COPY /frontend/. /app/
  RUN npm install && npm run build


# Set up Django / static serving of JavaScript app
FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

# Deal with the Django app
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN mkdir -p /static \
	&& mkdir /data \
	&& chown datapunt /data \
	&& chown datapunt /static

RUN mkdir -p /vue_static && chown datapunt /vue_static

WORKDIR /app
COPY ./web/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

USER datapunt
COPY ./web/app/ /app/
COPY ./web/deploy/ /deploy/

RUN export DJANGO_SETTINGS_MODULE=onderwijs.settings
RUN python manage.py collectstatic

# Now deal with the Vue app

COPY --from=builder /app/dist/ /vue_static/
# Production no waits / migrates etc.
CMD ["/deploy/docker-run.sh"]
