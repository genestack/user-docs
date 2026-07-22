---
diataxis: how-to
tab: odm-api
---

# How to process a 10x Genomics H5 file

This guide explains how to ingest a 10x Genomics H5 file through the ODM single-cell transformation pipeline.

## Required configuration change

Set `file_type` to `"h5"` instead of `"h5ad"`. Use the same H5AD key names (`obs`, `var`) in `metadata_keys`: the transformation converts the 10x H5 format to H5AD internally before applying unified processing.

```json
{
  "file_type": "h5",
  "cell_metadata": {
    "metadata_keys": {
      "obs": "metadata"
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

## Volume sizing

When setting `volume_size` for a job using an H5 input file, allocate at least 4× the original attachment size (for example, a 5 GB file requires `volume_size` ≥ 20 GB). H5 inputs require additional scratch space because the transformation converts them to H5AD during processing.

## Legacy 10x H5 support

Legacy 10x Genomics H5 files (v<3) are supported only when the file contains a single genome. If the file includes multiple genomes, pre-process it to extract the genome of interest before running the transformation.

## Prerequisites and workflow

For the full job submission workflow, see [How to run a transformation](../how-to-run-a-transformation.md). For authentication prerequisites, see [Authentication and tokens](../../../getting-started/authentication-and-tokens.md).

## Related

- [About single-cell transformations](about-single-cell-transformations.md): supported input formats overview.
- [Available images reference](../available-images-reference.md): volume sizing guidance.
- [Configuration reference](configuration-reference.md)
