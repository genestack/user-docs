---
diataxis: how-to
tab: odm-api
---

# How to ingest cell and expression data from an H5AD file

This guide explains how to add a single-cell layer (Cell Group and Expression Group) to a study that already has Sample, Library, or Preparation groups in ODM.

## When to use this

Use this guide when your study already has SLP groups in ODM and you need to add single-cell data on top of them.

If your study does not yet have SLP groups, see [Create Sample, Library, or Preparation groups from your H5AD file](create-sample-library-preparation-groups.md) instead.

## Prerequisites

- An API token and Curator group membership. See [Authentication and tokens](../../../getting-started/authentication-and-tokens.md).
- The HDF5 file uploaded as an attachment to your study in ODM.
- Sample, Library, or Preparation groups already present in the study.

For the full job submission workflow, see [How to run a transformation](../how-to-run-a-transformation.md).

## Configuration

Configure `cell_metadata`, `feature_metadata`, and `cell_expression` in your configuration's `data` field:

```json
{
  "file_type": "h5ad",
  "cell_metadata": {
    "metadata_keys": {
      "obs": "metadata",
      "obsm": "embedding"
    },
    "columns_to_drop": ["taxon", "organism_id"],
    "columns_renaming_map": {
      "sample": "batch",
      "pctmt": "percentMito"
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

- `columns_to_drop`: list of cell metadata columns to exclude from import.
- `columns_renaming_map`: map of source column names to target names in ODM.

## Linking resolution

The transformation resolves the parent SLP entity for the created Cell Group automatically, in the order: Library → Preparation → Sample (it uses the first entity type it finds in the study).

To link to a specific group by accession, set `cell_metadata.linking_group` explicitly:

```json
"cell_metadata": {
  "linking_group": {
    "library": "GSFXXXXXX"
  }
}
```

To link to all Preparation groups in the study without specifying accessions individually, set an empty value:

```json
"cell_metadata": {
  "linking_group": {
    "preparation": []
  }
}
```

For the full linking resolution rules, see [Transformation process reference](transformation-process-reference.md).

## Related

- [How to run a transformation](../how-to-run-a-transformation.md)
- [Configure metadata curation](configure-metadata-curation.md)
- [Configuration reference](configuration-reference.md)
