---
diataxis: how-to
tab: api-libraries
---

# How to install ODM SDK

## Requirements

- Python 3
- pip

## Install the latest version

```shell
python3 -m pip install odm-sdk
```

## Install a specific version

To install a specific version, append the version number to the package name:

```shell
python3 -m pip install odm-sdk==1.57.0
```

## Check the installed version

```shell
python3 -m pip show --verbose odm-sdk
```

## Remove the package

```shell
python3 -m pip uninstall odm-sdk
```

## Next steps

After installing, configure the SDK with your ODM instance URL and credentials. See [Configure](configure.md).

If you encounter installation issues, see [Troubleshoot installation](troubleshoot-installation.md).
