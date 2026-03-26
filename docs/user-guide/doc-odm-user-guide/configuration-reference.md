# Configuration Reference: Single-Cell HDF5 Transformation

> **Related documentation:** For conceptual background, see [About Single-Cell HDF5 Transformations in ODM](about-sc-hdf5-transformations.md). For step-by-step usage, see the [How-to Guides](how-to-sc-hdf5-transformations.md). For the API endpoints used to store and submit configurations, see the [API Reference](api-reference.md). For the internal processing pipeline, see the [Transformation Process Reference](transformation-process-reference.md).

This reference describes all parameters accepted by the single-cell HDF5 transformation configuration file. Parameters are organized by top-level section. Required parameters are marked **mandatory**; all others are optional.

The configuration is validated at the start of every run. If `file_type` is missing or invalid, the pipeline raises an error immediately. For all other sections, all validation errors are collected and reported together at the end of validation, so the complete set of issues is visible in a single run.

Unrecognized keys are ignored with a warning logged.

---

## Top-level parameters

### `file_type`

| | |
|---|---|
| **Type** | `string` |
| **Required** | Yes |
| **Accepted values** | `"h5ad"`, `"h5"` |

Specifies the format of the input HDF5 file. Must be provided; the pipeline cannot proceed without a valid file type.

### `dry_run`

| | |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

When `true`, the transformation performs all extraction, validation, and linking resolution steps but does not upload any data to ODM and does not save logs as an attachment. Expression matrix compression is also skipped. Use to validate configuration before committing data.

### `save_logs`

| | |
|---|---|
| **Type** | `boolean` |
| **Default** | `true` |

When `false`, transformation logs are not saved as an attachment in ODM after the run completes. Has no effect when `dry_run` is `true`.

---

## `biosample_metadata`

Settings for extracting, transforming, and exporting cell-level metadata to Sample, Library, or Preparation entities. The entire section is optional. If present, the following parameters apply.

### `metadata_keys`

| | |
|---|---|
| **Type** | `dict[string, string]` |
| **Required** | Yes, if `biosample_metadata` is present |

Maps HDF5 group keys to metadata types. Use `"obs": "metadata"` to read standard cell metadata as the source for biosample-level aggregation.

Example:
```json
{
  "obs": "metadata"
}
```

### `biosample_column_name`

| | |
|---|---|
| **Type** | `string` |
| **Required** | Yes, if `biosample_metadata` is present |

The name of the column in the cell metadata that identifies which biosample each cell belongs to (for example, a sample ID, library ID, or preparation ID column). Rows are grouped by this column for biosample-level aggregation.

---

### `biosample_metadata.sample`

Settings for exporting metadata to the Sample entity. Optional.

#### `create_new_group`

| | |
|---|---|
| **Type** | `boolean` |

When `true`, the transformation creates a new Sample group in ODM and links it to the study. When omitted or `false`, the transformation updates existing Sample group objects instead of creating new ones.

#### `template_id`

| | |
|---|---|
| **Type** | `string` |

The template ID to apply when creating a new Sample group. If not specified, the study's default template is applied.

#### `columns_to_export`

| | |
|---|---|
| **Type** | `list[string]` |

List of cell metadata column names to include in the exported Sample metadata. Only columns that are constant per biosample (as identified by `biosample_column_name`) are eligible. Exported columns are automatically dropped from the cell metadata.

#### `columns_renaming_map`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Maps source column names to new names in the exported metadata.

Example:
```json
{
  "tissue_type": "tissueType"
}
```

#### `columns_to_fill_missing_values`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Specifies default values to use for missing entries in the listed columns.

Example:
```json
{
  "disease": "unknown"
}
```

#### `columns_to_curate_values`

| | |
|---|---|
| **Type** | `dict[string, dict[string, string]]` |

Maps specific values in a column to replacement values.

Example:
```json
{
  "tissue": {
    "PBMCs": "peripheral blood mononuclear cells"
  }
}
```

---

### `biosample_metadata.library`

Settings for exporting metadata to the Library entity. Optional. Accepts the same parameters as `biosample_metadata.sample`, plus:

#### `linking_group`

| | |
|---|---|
| **Type** | `string` |

Accession of an existing Sample group to link the new Library group to. If not specified, the pipeline uses: (1) a Sample group created in the same run, or (2) pre-fetched Sample group accessions for the study.

---

### `biosample_metadata.preparation`

Settings for exporting metadata to the Preparation entity. Optional. Accepts the same parameters as `biosample_metadata.library`, including `linking_group`.

> **Constraint:** Only one of `library` or `preparation` may have `columns_to_export` set in the same configuration.

---

## `cell_metadata`

Settings for extracting and transforming cell-level metadata. The entire section is optional. If absent, no Cell Group is created.

### `metadata_keys`

| | |
|---|---|
| **Type** | `dict[string, string]` |
| **Required** | Yes, if `cell_metadata` is present |

Maps HDF5 group keys to metadata types. At least one key with value `"metadata"` is required.

Accepted key-value pairs for H5AD files:

| Key | Value | Description |
|-----|-------|-------------|
| `obs` | `metadata` | Standard cell annotations |
| `obsm` | `embedding` | Multidimensional cell data (PCA, UMAP, etc.) |
| `obsp` | `pairwise` | Pairwise cell annotations (e.g., cell–cell distances) |

For H5 files, specify metadata using the same H5AD key names (`obs`, `obsm`, `obsp`). The transformation maps these to the correct internal structure regardless of source format.

Example:
```json
{
  "obs": "metadata",
  "obsm": "embedding",
  "obsp": "pairwise"
}
```

### `linking_group`

| | |
|---|---|
| **Type** | `dict[string, string \| list[string] \| null]` |

Specifies the parent SLP entity to which the Cell Group will be linked. Must contain exactly one key: `sample`, `library`, or `preparation`. The value is either a list of group accessions, a single accession string, or an empty value.

If an empty value is provided (`[]`, `""`, or `null`), the pipeline resolves all available group accessions of the specified entity type for the study.

If `linking_group` is absent and no new SLP groups are being created, auto-discovery applies: Library → Preparation → Sample, using the first entity type with at least one associated group.

Examples:
```json
{ "library": "GSF017080" }
```
```json
{ "preparation": [] }
```

### `columns_to_drop`

| | |
|---|---|
| **Type** | `list[string]` |

Column names to remove from the cell metadata before processing.

Example:
```json
["taxon", "organism_id"]
```

### `columns_renaming_map`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Maps source column names to new names.

Example:
```json
{
  "sample": "batch",
  "pctmt": "percentMito"
}
```

### `columns_to_fill_missing_values`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Default values for missing entries in the specified columns.

Example:
```json
{
  "batch": "unknown"
}
```

### `columns_to_curate_values`

| | |
|---|---|
| **Type** | `dict[string, dict[string, string]]` |

Replacement values for specific entries in specified columns.

Example:
```json
{
  "sample": {
    "LGVXCTRL1": "lung_healthy_1"
  }
}
```

### `set_column_value`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Sets a constant value for all rows in the specified columns. Can be used to add a new attribute column or overwrite an existing one.

Example:
```json
{
  "sample_id": "lung_1"
}
```

### `columns_to_preserve_name`

| | |
|---|---|
| **Type** | `list[string]` |

Column names to exempt from the internal attribute name standardization step. Use for columns whose names contain characters that would otherwise be altered (for example, Leiden cluster columns with decimal suffixes such as `cluster_leiden_0.5`).

Example:
```json
["cluster_leiden_0.5"]
```

### `add_qc_metrics`

| | |
|---|---|
| **Type** | `boolean` |
| **Default** | `true` |

When `true`, QC metrics are calculated and added to the cell metadata if not already present. QC metrics include number of counts, number of genes, and mitochondrial and ribosomal gene presence. When `false`, or when `dry_run` is `true`, QC calculation is skipped.

---

## `feature_metadata`

Settings for extracting and transforming feature (gene)-level metadata. The entire section is optional.

### `metadata_keys`

| | |
|---|---|
| **Type** | `dict[string, string]` |
| **Required** | Yes, if `feature_metadata` is present |

Maps HDF5 group keys to metadata types. At least one key with value `"metadata"` is required.

Accepted key-value pairs for H5AD files:

| Key | Value | Description |
|-----|-------|-------------|
| `var` | `metadata` | Standard feature annotations |
| `varm` | `embedding` | Multidimensional feature data |
| `varp` | `pairwise` | Pairwise feature annotations |

For H5 files, specify metadata using the same H5AD key names (`var`, `varm`, `varp`). The transformation maps these to the correct internal structure regardless of source format.

Example:
```json
{
  "var": "metadata",
  "varm": "embedding"
}
```

### `columns_to_drop`

| | |
|---|---|
| **Type** | `list[string]` |

Column names to remove from the feature metadata.

### `columns_renaming_map`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Maps source column names to new names.

### `columns_to_fill_missing_values`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Default values for missing entries in the specified columns.

### `columns_to_curate_values`

| | |
|---|---|
| **Type** | `dict[string, dict[string, string]]` |

Replacement values for specific entries in specified columns.

### `set_column_value`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Sets a constant value for all rows in the specified columns.

### `columns_to_preserve_name`

| | |
|---|---|
| **Type** | `list[string]` |

Column names to exempt from the internal attribute name standardization step.

### `map_gene_ids_to_names`

| | |
|---|---|
| **Type** | `boolean` |
| **Default** | `true` |

When `true`, the transformation attempts to map gene IDs to gene names if gene names are absent and the standard `geneId` column is present. The pipeline infers the ID source (Ensembl or NCBI) and the species automatically. When `false`, gene ID mapping is skipped. Set to `false` for proteomics or other omics data that do not use gene IDs as identifiers.

> The gene ID column must use the standard name `geneId` for mapping to be performed.

**Supported organisms and annotation releases (hdf5-cells v0.0.4):**

| Organism | Genome version | Ensembl release | NCBI release |
|----------|---------------|-----------------|--------------|
| *Homo sapiens* | GRCh38.p14 | 115 | GCF_000001405.40-RS_2025_08 |
| *Mus musculus* | GRCm39 | 115 | GCF_000001635.27-RS_2024_02 |
| *Rattus norvegicus* | GRCr8 | 115 | GCF_036323735.1-RS_2024_02 |
| *Sus scrofa* | Sscrofa11.1 | 115 | 106 |

---

## `cell_expression`

Settings for extracting and uploading the cell expression matrix. The entire section is optional. If absent, no Expression Group is created.

### `data_class`

| | |
|---|---|
| **Type** | `string` |
| **Required** | Yes, if `cell_expression` is present |

The data class label for the expression data.

Example:
```json
"Single-cell transcriptomics"
```

### `compression_level`

| | |
|---|---|
| **Type** | `integer` (0–9) |
| **Default** | `4` |

Controls the Brotli compression level for the output expression file. Higher values produce smaller files at the cost of longer compression time.

### `chunk_size`

| | |
|---|---|
| **Type** | `integer` |

Number of features processed per chunk during expression data export. If not specified, the value is calculated automatically from available container memory.

### `max_buffer_size`

| | |
|---|---|
| **Type** | `integer` |
| **Default** | `50` |

Controls how much data is held in memory before being flushed to disk during expression writing.

### `number_format`

| | |
|---|---|
| **Type** | `string` |

Controls the numeric precision of values in the output file. Accepts either a printf-style format string (e.g. `"%.7g"`, `"%d"`) or a NumPy dtype string (e.g. `"float32"`, `"int64"`). If not set, the format is inferred from the data.

### `columns_to_drop`

| | |
|---|---|
| **Type** | `list[string]` |

Column names to remove from the expression metadata.

### `columns_renaming_map`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Maps source column names to new names in the expression metadata.

### `set_column_value`

| | |
|---|---|
| **Type** | `dict[string, string]` |

Sets a constant value for all rows in the specified expression metadata columns.

### `source_file_metadata`

| | |
|---|---|
| **Type** | `boolean` |
| **Default** | `true` |

When `true`, metadata from the source HDF5 attachment is read and included in the expression metadata (subject to `columns_to_drop`, `columns_renaming_map`, and `set_column_value`). When `false`, source file metadata extraction is skipped.

In all cases, the following statistics are always computed and appended to the expression metadata regardless of this flag: total number of cells, total number of features, sparsity (%), number of non-zero values, source file accession, and source file name.
