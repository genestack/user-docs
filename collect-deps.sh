#!/usr/bin/env sh

set -eux

export ODM_API_PYTHON_DIR=docs/tools/odm-api/python/generated
export ODM_API_R_DIR=docs/tools/odm-api/r/generated
export ODM_SDK_DIR=docs/tools/odm-sdk/generated

rm -rf $ODM_API_PYTHON_DIR $ODM_API_R_DIR $ODM_SDK_DIR
mkdir -p $ODM_API_PYTHON_DIR $ODM_API_R_DIR $ODM_SDK_DIR

curl -v -L --user "$NEXUS_USER:$NEXUS_PASSWORD" "$RAW_REGISTRY_SNAPSHOTS/docs/odm-api-python/odm-api-python-$OPENAPI_VERSION.tar.gz" -o "$ODM_API_PYTHON_DIR/archive.tar.gz"
curl -v -L --user "$NEXUS_USER:$NEXUS_PASSWORD" "$RAW_REGISTRY_SNAPSHOTS/docs/odm-api-r/odm-api-r-$OPENAPI_VERSION.tar.gz" -o "$ODM_API_R_DIR/archive.tar.gz"
curl -v -L --user "$NEXUS_USER:$NEXUS_PASSWORD" "$RAW_REGISTRY_SNAPSHOTS/docs/odm-sdk/odm-sdk-$SDK_VERSION.tar.gz" -o "$ODM_SDK_DIR/archive.tar.gz"

cd $ODM_API_PYTHON_DIR && tar xf archive.tar.gz && cd $OLDPWD
cd $ODM_API_R_DIR && tar xf archive.tar.gz && cd $OLDPWD
cd $ODM_SDK_DIR && tar xf archive.tar.gz && cd $OLDPWD
