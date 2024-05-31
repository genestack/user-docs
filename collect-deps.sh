#!/usr/bin/env sh

set -eu

export ODM_API_PYTHON_DIR=docs/tools/odm-api/python/generated
export ODM_API_R_DIR=docs/tools/odm-api/r/generated
export ODM_SDK_DIR=docs/tools/odm-sdk/generated
export USER_GUIDE_DIR=docs/user-guide

rm -rf $ODM_API_PYTHON_DIR $ODM_API_R_DIR $ODM_SDK_DIR $USER_GUIDE_DIR
mkdir -p $ODM_API_PYTHON_DIR $ODM_API_R_DIR $ODM_SDK_DIR $USER_GUIDE_DIR

curl -v -L --user "$NEXUS_USER:$NEXUS_PASSWORD" "$RAW_REGISTRY_SNAPSHOTS/docs/odm-api-python/odm-api-python-$OPENAPI_VERSION.tar.gz" -o "$ODM_API_PYTHON_DIR/archive.tar.gz"
curl -v -L --user "$NEXUS_USER:$NEXUS_PASSWORD" "$RAW_REGISTRY_SNAPSHOTS/docs/odm-api-r/odm-api-r-$OPENAPI_VERSION.tar.gz" -o "$ODM_API_R_DIR/archive.tar.gz"
curl -v -L --user "$NEXUS_USER:$NEXUS_PASSWORD" "$RAW_REGISTRY_SNAPSHOTS/docs/odm-sdk/odm-sdk-$SDK_VERSION.tar.gz" -o "$ODM_SDK_DIR/archive.tar.gz"
curl -v -L --user "$NEXUS_USER:$NEXUS_PASSWORD" "$RAW_REGISTRY_SNAPSHOTS/docs/user-guide/user-guide-$USER_GUIDE_VERSION.tar.gz" -o "$USER_GUIDE_DIR/archive.tar.gz"

cd $ODM_API_PYTHON_DIR && tar xf archive.tar.gz && cd $OLDPWD
cd $ODM_API_R_DIR && tar xf archive.tar.gz && cd $OLDPWD
cd $ODM_SDK_DIR && tar xf archive.tar.gz && cd $OLDPWD
cd $USER_GUIDE_DIR && tar xf archive.tar.gz && cd $OLDPWD
