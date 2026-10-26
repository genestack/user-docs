---
diataxis: how-to
tab: api-libraries
---

# Delete a study

This guide explains how to delete a study from ODM using the `odm-delete-study` script.

## Prerequisites

- Configured ODM SDK. See [Configure the ODM SDK](../configure.md).
- Ownership of the study, and a Bearer token or API token. See [Authentication and tokens](../../../odm-api/getting-started/authentication-and-tokens.md).

> **Warning:**
>
> 1. Only the study owner can delete a study and its child objects. No role grants this right.
> 2. The script does not verify that the file with the provided accession exists. If nothing is deleted but the script runs without error, it will still output `Success`.
> 3. The script does not check the type of the object. If a template's accession is provided instead of a study's accession and you hold the "Template Administrator" role, the template will be deleted. For deleting templates, use the script described in [Delete a template](../templates/delete-a-template.md).

## Steps

1. Explore script options:

    ```shell
    odm-delete-study -h
    ```

2. Run the script with the study accession. The script prints `Success` or an error stack trace:

    ```shell
    odm-delete-study --accession GSF244344 -H HOSTNAME
    ```

## Related

- [Delete a template](../templates/delete-a-template.md)
