---
diataxis: how-to
tab: api-libraries
---

# Install

This guide explains how to install the ODM Python API Client (`odm-api`).

## Requirements

- Python 3
- pip

## Install the package

Open a terminal and run:

```shell
python3 -m pip install odm-api
```

To install a specific version, append the version number to the package reference:

```shell
python3 -m pip install odm-api==1.57.0
```

## Check the installed version

```shell
python3 -m pip show --verbose odm-api
```

This also lists all available console commands provided by the package.

## Uninstall

```shell
python3 -m pip uninstall odm-api
```

## Next steps

See [Usage example](usage-example.md) for a worked example of authenticating and calling an API endpoint.
