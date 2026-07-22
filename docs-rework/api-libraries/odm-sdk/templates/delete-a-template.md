---
diataxis: how-to
tab: api-libraries
---

# How to delete a template

This guide explains how to delete a template from ODM using the `odm-delete-template` script.

## Prerequisites

- Configured ODM SDK. See [Configure](../configure.md).
- "Manage organisation" permission and a Bearer token or API token. See [Authentication and tokens](../../../odm-api/getting-started/authentication-and-tokens.md).

> **Warning:**
> 1. The Default template can be deleted, which may cause issues, so be careful.
> 2. Only users with the "Manage organization" permission can delete templates.
> 3. The script does not verify that the file with the provided accession exists. If nothing is deleted but the script runs correctly, it will still output `Success`.
> 4. The script does not check the type of the object. If a study's accession is provided instead of a template's accession, the study will be deleted. For deleting studies, use the script described in [Delete a study](../study/delete-a-study.md).

## Steps

1. Before deleting a template, manually change the template on all studies that currently use it. Apply a different template (for example, the Default template) via the ODM user interface.

2. Explore script options:

   ```shell
   odm-delete-template -h
   ```

3. Run the delete script with the template accession:

   ```shell
   odm-delete-template --accession GSF244345 -H GENESTACK_ENDPOINT_ADDR
   ```

   Where `GENESTACK_ENDPOINT_ADDR` is the URL of your ODM instance. The script prints `Success` or an error stack trace.

## Related

- [Create or update a template](create-or-update-a-template.md)
- [Delete a study](../study/delete-a-study.md)
