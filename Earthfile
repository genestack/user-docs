VERSION 0.8

ARG --global --required HARBOR_DOCKER_REGISTRY

build:
    FROM python:3.14.8-alpine
    WORKDIR /app

    COPY requirements.txt .
    RUN python3 -m pip install --no-cache-dir -r requirements.txt

    COPY --dir docs-rework mkdocs.yml .
    RUN mkdocs build

    SAVE ARTIFACT site

image:
    FROM nginxinc/nginx-unprivileged:1.31.6-alpine
    COPY fs /
    COPY --pass-args +build/site/ /usr/share/nginx/html/

    ARG --required USER_DOCS_VERSION
    SAVE IMAGE --push ${HARBOR_DOCKER_REGISTRY}/user-docs:${USER_DOCS_VERSION}
    SAVE IMAGE --push ${HARBOR_DOCKER_REGISTRY}/user-docs:latest

main:
    BUILD +image
