# How to discover which biosample attributes are available

This guide explains how to use a dry-run job to identify which cell-level metadata columns are uniform per biosample in your HDF5 file, so you can plan your `columns_to_export` before a full run.

## When to use this

Use this when you are planning a biosample export and want to know which attributes are available before committing to a `columns_to_export` list. No data is created or updated in ODM.

## Prerequisites

- An API token and Curator group membership. See [Authentication and tokens](../../getting-a-genestack-api-token.md).
- The HDF5 file uploaded as an attachment to your study.

## Configuration (discovery mode)

Configure `biosample_metadata` with `metadata_keys` and `biosample_column_name`, and leave out `columns_to_export`. Discovery analyses column uniformity across all `obs` columns relative to `biosample_column_name` and is entity-agnostic, so no Sample, Library, or Preparation entity object is needed:

```json
{
  "file_type": "h5ad",
  "biosample_metadata": {
    "metadata_keys": {
      "obs": "metadata"
    },
    "biosample_column_name": "sample_id"
  }
}
```

Set `biosample_column_name` to a column that actually exists in your file's `obs`. If the named column is not present in the cell metadata, the job aborts with an error.

## Submit as a dry run

When submitting the job, set `dry_run: true` in the request body. Dry-run mode is required for this step: the uniform-attribute report is produced only when `dry_run` is `true`. A normal run with no `columns_to_export` produces no report. For the full submission steps, see [How to run a transformation](../how-to-run-a-transformation.md).

## What the logs report

The transformation logs include:

- The number of unique biosamples found.
- The list of columns that are constant across all cells per biosample (eligible for export).

No ODM objects are created or modified.

## Next steps

Use the logged list to plan your `columns_to_export` configuration, then move to:

- [Create Sample, Library, or Preparation groups](create-sample-library-preparation-groups.md): if SLP groups do not yet exist.
- [Update existing biosample metadata](update-existing-biosample-metadata.md): if SLP groups already exist.
