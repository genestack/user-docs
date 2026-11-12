# syntax=docker/dockerfile:1.28
#
# The ODM user documentation: the MkDocs site built from docs-rework/ and mkdocs.yml,
# served by its own nginx on 8080 (fs/etc/nginx/conf.d/default.conf). The build context is
# this repo, filtered by .dockerignore. The Makefile builds one target:
#
#   push  the image CI publishes and the odm chart deploys
#
# The repo has no tests: `make test` builds push with no output.

ARG PYTHON_IMAGE=python:3.15.2-alpine
ARG NGINX_IMAGE=nginxinc/nginx-unprivileged:1.31.7-alpine

FROM ${PYTHON_IMAGE} AS build

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY docs-rework/ docs-rework/
COPY mkdocs.yml .
RUN mkdocs build

# Last, so that a plain `docker build .` gives this image.
FROM ${NGINX_IMAGE} AS push

COPY fs /
COPY --from=build /app/site/ /usr/share/nginx/html/
