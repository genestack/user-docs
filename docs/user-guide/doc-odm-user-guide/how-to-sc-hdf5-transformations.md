# How-to Guides: Single-Cell HDF5 Transformations in ODM

These guides show how to accomplish specific tasks using the single-cell HDF5 transformation. Each guide assumes you have a valid input file (H5AD or 10x H5) already attached to a study in ODM.

For a conceptual overview of the entities involved and how the transformation works, see [About Single-Cell HDF5 Transformations in ODM](about-sc-hdf5-transformations.md). For the full list of configuration parameters, see the [Configuration Reference](configuration-reference.md). For the API endpoint specifications, see the [API Reference](api-reference.md). For details on what the pipeline does internally at each stage, see the [Transformation Process Reference](transformation-process-reference.md).

---

## How to run a transformation via the ODM API

This guide covers the end-to-end steps to ingest single-cell data into ODM using the Processors Controller API. The process involves three steps: creating a configuration, running a dry run to validate it, and submitting the full run.

### Step 1: Create a transformation configuration

Create a configuration document that describes how to process your file. The `data` field contains the processing specification; the `name` and `description` are for your own reference.

```
POST /api/v1/transformations/configurations
```

```json
{
  "name": "my_study_config",
  "description": "Cell and expression ingestion for study XYZ",
  "data": {
    "file_type": "h5ad",
    "cell_metadata": {
      "metadata_keys": {
        "obs": "metadata",
        "obsm": "embedding"
      },
      "columns_to_drop": ["taxon"],
      "columns_renaming_map": {
        "sample": "batch"
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
}
```

The response includes the `id` of the created configuration. It is required for subsequent steps.

For a full description of the `data` object, see the [Configuration Reference](configuration-reference.md).

For a default configurations prepared, see the [Configuration mapping](doc-odm-user-guide/extras/public-dataset-configurations-mapping.md)

### Step 2: Identify the transformation image

```
GET /api/v1/transformations/images
```

Confirm that the `hdf5-cells` image is available. Note the version you want to use: typically `"latest"`, or a specific release tag for reproducibility.

### Step 3: Submit a dry-run job

```
POST /api/v1/transformations/jobs
```

```json
{
  "configuration_id": <config_id>,
  "dry_run": true,
  "image_reference": {
    "name": "hdf5-cells",
    "version": "latest"
  },
  "input_accessions": ["<attachment_accession>"],
  "volume_size": 30
}
```

As a guideline for setting `volume_size`:
- For H5AD input files, allocate approximately **1.4× the size of the original attachment** (in GB).
- For 10x H5 input files, allocate at least **4× the size of the original attachment** (in GB).

The response includes the `id` of the created job. It is required for subsequent steps.

### Step 4: Monitor the dry-run job

```
GET /api/v1/transformations/jobs/{job_id}
```

Repeat until `status.state` reaches a terminal value: `DONE` or `FAILED`.

### Step 5: Review the logs

```
POST /api/v1/transformations/jobs/{job_id}/logs
```

Review the logs for warnings and errors. Pay particular attention to:
- Configuration validation messages.
- The file structure report: which metadata keys are present in your file.
- Linking validation results: whether all cell `batch` values map to existing SLP objects.
- Any columns flagged for automatic renaming or data type conversion.

If issues are found, update the configuration and repeat from Step 3. See [How to iterate on a configuration using dry runs](#how-to-iterate-on-a-configuration-using-dry-runs) for the recommended cycle.

### Step 6: Submit the full run

Once the dry run completes without issues, submit the same job with environment variable `dry_run` set to `false`:

```
POST /api/v1/transformations/jobs
```

```json
{
  "configuration_id": <config_id>,
  "dry_run": false,
  "image_reference": {
    "name": "hdf5-cells",
    "version": "latest"
  },
  "input_accessions": ["<attachment_accession>"],
  "volume_size": 30
}
```

Monitor and retrieve logs the same way as the dry run (Steps 4–5). When the job completes, the logs contain the ODM accessions assigned to each object that was created or updated. The logs are uploaded as attachment to the same study.

---

## How to iterate on a configuration using dry runs

This guide describes the recommended iterative cycle for refining a transformation configuration before committing to a full run. Use this when the initial dry run reveals warnings or errors that require attention.

The cycle follows this pattern:

```
Create configuration → Submit dry-run job → Review logs
       ↑                                          |
       └──── Update configuration ←──────────────┘
              (if issues found)
```

After reviewing the logs from a dry-run job, update the existing configuration using:

```
PUT /api/v1/transformations/configurations/{config_id}
```

The request body follows the same structure as the original `POST`. The configuration at the given `id` is fully replaced with the new content.

Then resubmit the dry-run job with the same `configuration_id`. Because the configuration is updated in place, you can reuse the same `configuration_id` across all iterations without creating a new configuration for each attempt.

Repeat until the dry run completes without errors or warnings that require action. Then submit the full run.

---

## How to ingest cell and expression data from an H5AD file

Use this when the study already has Sample, Library, or Preparation groups in ODM and you only need to add the single-cell layer. Configure `cell_metadata`, `feature_metadata`, and `cell_expression` in your configuration's `data` field.

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

The transformation resolves the linking target for created Cell Group automatically in the following order: Library → Preparation → Sample. To link to a specific group, set `cell_metadata.linking_group` explicitly:

```json
"cell_metadata": {
  "linking_group": {
    "library": "GSFXXXXXX"
  }
}
```

To link to all preparation groups in the study without specifying their accessions individually, set an empty value:

```json
"cell_metadata": {
  "linking_group": {
    "preparation": []
  }
}
```

---

## How to create Sample, Library, or Preparation groups from your H5AD file

Use this when your study does not yet have SLP groups in ODM and you want to derive biosample-level attributes from the cell metadata.

Identify the column in your cell metadata that acts as a biosample identifier. Set this as `biosample_column_name`. Under the relevant entity (`sample`, `library`, or `preparation`), set `create_new_group: true` and list the columns to export under `columns_to_export`.

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

The transformation aggregates cells by `biosample_column_name` and exports only attributes that are constant per biosample. Exported columns are automatically removed from the cell metadata.

Only one of `library` or `preparation` may have `columns_to_export` set in the same configuration.

To create a Library group without exporting attributes (a placeholder group used only for linking), set `create_new_group: true` and omit `columns_to_export`:

```json
"library": {
  "create_new_group": true
}
```

---

## How to update existing biosample metadata

Use this when SLP groups already exist in ODM but are missing attributes that are present in your HDF5 file.

Configure `biosample_metadata` with `columns_to_export` for the target entity, but do not set `create_new_group: true`.

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

The transformation matches extracted rows to existing ODM objects on the entity ID column and updates only attributes that do not already exist. If any extracted ID does not match an existing ODM object, the transformation raises an error. Run a dry run first to catch ID mismatches before committing data.

---

## How to discover which biosample attributes are available in your file

Use this to identify which cell-level metadata columns are uniform per biosample and can be exported. No data will be updated in ODM.

Submit a dry-run job with `biosample_metadata` configured but without any `columns_to_export` entries:

```json
{
  "file_type": "h5ad",
  "biosample_metadata": {
    "metadata_keys": {
      "obs": "metadata"
    },
    "biosample_column_name": "sample_id",
    "sample": {}
  }
}
```

The transformation logs the number of unique biosamples found and the list of columns that are constant across all cells per biosample. Use the logged list to plan your `columns_to_export` configuration before running a full ingestion.

---

## How to process a 10x Genomics H5 file

The only required change compared to an H5AD configuration is setting `file_type` to `"h5"`. Use the same H5AD key names (`obs`, `var`) in `metadata_keys` — the transformation converts the 10x H5 format to H5AD internally and applies unified processing.

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

Volume sizing for .h5 inputs: When setting `volume_size` for a job that uses an H5 input file, allocate at least **4× the original attachment size (e.g., a 5 GB file → volume_size ≥ 20 GB). H5 inputs require additional scratch space because the transformation converts them to H5AD during processing.

Legacy 10x H5 support: Legacy 10x Genomics H5 files (v<3) are supported only when the file contains a single genome. If the file includes multiple genomes, pre-process it to extract the genome of interest before running the transformation.

---

## How to configure metadata curation

These operations are available in `cell_metadata`, `feature_metadata`, and per-entity settings within `biosample_metadata`. They are applied in the order listed.

**To drop columns:**

```json
"columns_to_drop": ["taxon", "organism_id"]
```

**To rename a column:**

```json
"columns_renaming_map": {
  "sample": "batch",
  "pctmt": "percentMito"
}
```

**To replace specific values:**

```json
"columns_to_curate_values": {
  "sample": {
    "LGVXCTRL1": "lung_healthy_1"
  }
}
```

**To fill missing values:**

```json
"columns_to_fill_missing_values": {
  "batch": "unknown"
}
```

**To set a constant value for all rows:**

```json
"set_column_value": {
  "sample_id": "lung_1"
}
```

After all explicit column operations, matching attributes are mapped to ODM standard names. The rest are converted to camelCase. Columns listed in `columns_to_preserve_name` are exempt from this standardization step.

For the details, see [Attribute Mapping Reference](docs/user-guide/doc-odm-user-guide/attribute-mapping.md)

**To prevent a column from being automatically renamed:**

```json
"columns_to_preserve_name": ["cluster_leiden_0.5"]

For full parameter specifications, see the [Configuration Reference](configuration-reference.md).
