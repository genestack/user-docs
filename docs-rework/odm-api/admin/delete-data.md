---
diataxis: how-to
tab: odm-api
---

# How to delete data

Deletion is how you permanently remove data from ODM, whether you are clearing out the detached debris of a failed import or retiring data you no longer need. A single call can take a lot with it, so it is worth knowing exactly what cascades before you run one.

> **Warning:** Deletion is irreversible. Deleted objects and their linked data cannot be recovered.

For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token. See [Authentication and tokens](../getting-started/authentication-and-tokens.md).
- "Manage organisation" AND "Access all data" permissions.

## Delete an object

To delete an object, call `DELETE /api/v1/manage-data/data` with the Genestack accession of the object or group in the request body. For example, to delete the study `GSF1147012`:

```json
{
  "accession": "GSF1147012"
}
```

A `202` response confirms the request was accepted. Deletion then runs asynchronously, so to confirm it finished, search for the object in the Study Browser or via the API; it should no longer appear.

## What a delete takes with it

Deletion cascades down the data model. Deleting a study removes everything linked to it: sample groups, library groups, preparation groups, tabular data, VCF data, flow cytometry data, and attached files. Deleting a signal group removes the group along with all of its associated data objects.

You can delete:

- Studies and all their linked entities.
- Sample groups, library groups, and preparation groups.
- Tabular data (expression), gene variant data, and flow cytometry data.
- Cell metadata groups and cell expression groups.
- Reference genomes (see the note below).
- Attached files (available since release 1.59).

## Deleting a reference genome

If you delete a reference genome that is linked to any VCF groups, gene-name-based variant search (`variantFeature`) becomes unavailable for those VCF groups.

## S3 cleanup

When you delete a data file that was imported from a local computer, ODM automatically removes the corresponding file from S3 (since release 1.60).

## Related

- [Find detached objects](find-detached-objects.md), identify orphaned objects before deletion.
- [Authentication and tokens](../getting-started/authentication-and-tokens.md)
