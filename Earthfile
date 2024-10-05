VERSION 0.8

ARG --global --required HARBOR_DOCKER_REGISTRY
ARG --global --required RAW_REGISTRY_SNAPSHOTS

build:
    FROM python:3.12.6-alpine
    DO github.com/genestack/earthly-libs+PYTHON_PREPARE

    COPY requirements.txt .
    RUN \
        --secret NEXUS_USER \
        --secret NEXUS_PASSWORD \
            pypi-login.sh && \
            python3 -m pip install --no-cache-dir -r requirements.txt && \
            apk add curl && \
            pypi-clean.sh

    ARG --required SDK_VERSION
    ARG --required OPENAPI_VERSION
    COPY collect-deps.sh .
    RUN \
        --secret NEXUS_USER \
        --secret NEXUS_PASSWORD \
            ./collect-deps.sh

    COPY --dir docs mkdocs.yml .
    RUN mkdocs build

    SAVE ARTIFACT site

image:
    FROM nginxinc/nginx-unprivileged:1.27.2-alpine
    COPY fs /
    COPY --pass-args +build/site/ /usr/share/nginx/html/

    ARG --required USER_DOCS_VERSION
    SAVE IMAGE --push ${HARBOR_DOCKER_REGISTRY}/user-docs:${USER_DOCS_VERSION}
    SAVE IMAGE --push ${HARBOR_DOCKER_REGISTRY}/user-docs:latest

main:
    BUILD +image
