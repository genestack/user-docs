---
sources:
  - path: docs/user-guide/doc-odm-user-guide/how-to-sc-hdf5-transformations.md
    lines: [223, 272]
diataxis: how-to
tab: odm-api
task: task-099
---

# How to create Sample, Library, or Preparation groups from an H5AD file

This guide explains how to derive Sample, Library, or Preparation (SLP) groups in ODM from biosample-level attributes stored in the cell metadata of your HDF5 file.

## When to use this

Use this guide when your study does not yet have SLP groups in ODM and your HDF5 file contains biosample-level attributes (such as tissue, disease, or donor_id) repeated per cell that you want to promote into ODM entities.

If SLP groups already exist and you only need to add single-cell data, see [Ingest cell and expression data from an H5AD file](ingest-cell-and-expression.md) instead.

## Prerequisites

- An API token and Curator group membership. See [Authentication and tokens](../../../getting-started/authentication-and-tokens.md).
- The HDF5 file uploaded as an attachment to your study in ODM.

For the full job submission workflow, see [How to run a transformation](../how-to-run-a-transformation.md).

## Configuration

Identify the column in your cell metadata that acts as the biosample identifier. Set it as `biosample_column_name`. Under the relevant entity (`sample`, `library`, or `preparation`), set `create_new_group: true` and list the columns you want to export:

```json
{
  "file_type": "h5ad",
  "biosample_metadata": {
    "metadata_keys": {
      "obs": "metadata"
    },
    "biosample_column_name": "sample_id",
    "sample": {
      "create_new_group": true,
      "columns_to_export": ["tissue", "disease", "donor_id"]
    }
  },
  "cell_metadata": {
    "metadata_keys": {
      "obs": "metadata",
      "obsm": "embedding"
    }
  },
  "feature_metadata": {
    "metadata_keys": {
      "var": "metadata"
    }
  },
  "cell_expression": {
    "data_class": "Single-cell transcriptomics"
  }
}
```

The `cell_metadata`, `feature_metadata`, and `cell_expression` sections are included because a single-cell run normally creates the SLP groups, Cell Group, and Expression Group together — the Cell Group needs an SLP parent to link to. Omit those sections if you only want to create SLP groups.

The transformation aggregates cells by `biosample_column_name`. It exports the columns you list in `columns_to_export`; each must be constant across all cells within a biosample, or the job fails. Use the [discovery dry-run](discover-biosample-attributes.md) first to find eligible columns. Exported columns are automatically removed from the cell metadata.

**Constraint:** only one of `library` or `preparation` may be created or updated in the same configuration — that is, only one may carry `create_new_group` or `columns_to_export`.

## Create a placeholder group for linking only

If you need a Library group to exist for linking purposes but do not need to export any attributes from it, set `create_new_group: true` and omit `columns_to_export`:

```json
"library": {
  "create_new_group": true
}
```

## Related

- [Discover which biosample attributes are available](discover-biosample-attributes.md) — use a dry run to identify which columns are uniform per biosample before committing to `columns_to_export`.
- [Configuration reference](configuration-reference.md) — full `biosample_metadata` block schema.
- [Transformation process reference](transformation-process-reference.md)
