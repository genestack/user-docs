# How to update existing biosample metadata

This guide explains how to enrich existing Sample, Library, or Preparation (SLP) groups in ODM with attributes derived from your HDF5 file.

## When to use this

Use this guide when SLP groups already exist in ODM but are missing attributes that are present in the cell metadata of your HDF5 file.

If no SLP groups exist yet, see [Create Sample, Library, or Preparation groups from an H5AD file](create-sample-library-preparation-groups.md) instead.

## Prerequisites

- An API token and Curator group membership. See [Authentication and tokens](../../getting-a-genestack-api-token.md).
- The HDF5 file uploaded as an attachment to your study.
- Existing SLP groups in ODM.

For the full job submission workflow, see [How to run a transformation](../how-to-run-a-transformation.md).

## Configuration

Configure `biosample_metadata` with `columns_to_export` for the target entity. Do **not** set `create_new_group: true`, which would create new groups instead of updating existing ones:

```json
{
  "file_type": "h5ad",
  "biosample_metadata": {
    "metadata_keys": {
      "obs": "metadata"
    },
    "biosample_column_name": "library_id",
    "library": {
      "columns_to_export": ["sequencing_platform", "library_strategy"]
    }
  }
}
```

## Matching behaviour

The transformation matches extracted rows to existing ODM objects using the entity ID column (Sample Source ID, Library ID, or Preparation ID). Only attributes that do not already exist in the ODM metadata are added. If any extracted ID does not match an existing ODM object, the transformation raises an error.

## Recommendation

Run a dry run first to catch ID mismatches before committing data. See [Manage configurations](../manage-configurations.md) for the recommended iteration loop.

## Related

- [Configure metadata curation](configure-metadata-curation.md)
- [Iterate with dry runs](iterate-with-dry-runs.md)
- [Configuration reference](configuration-reference.md)
