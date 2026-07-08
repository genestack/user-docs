# How to discover which biosample attributes are available

This guide explains how to identify which cell-level metadata columns are uniform per biosample in your HDF5 file - that is, attributes such as sex or disease that have the same value for every cell belonging to the same biosample. Rather than storing these attributes redundantly for each cell, you can promote them to the appropriate biosample level (Sample, Library, or Preparation) during the transformation, using `columns_to_export`. This dry-run discovery step lets you identify which columns are eligible before committing to a full run.

## When to use this

Use this when you are planning a biosample export and want to know which attributes are available before committing to a `columns_to_export` list. No data is created or updated in ODM.

## Prerequisites

- An API token and Curator group membership. See [Authentication and tokens](../../getting-a-genestack-api-token.md).
- The HDF5 file uploaded as an attachment to your study.

## Configuration (discovery mode)

Configure biosample_metadata with metadata_keys and biosample_column_name, but leave columns_to_export undefined on all entities, and submit the job with dry_run: true:

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

In this mode the pipeline analyses which obs columns are uniform per biosample value - that is, which attributes have a consistent value across all cells belonging to the same biosample. The results are written to the job log: the number of biosamples detected and the list of uniform attributes. No data is written to ODM and no groups are created or updated.

> **Note:** `biosample_column_name` must refer to a column that exists in your file's `obs` and contains the biosample identifier for each cell. If the column is not present, the job fails with an error.

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
