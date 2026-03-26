# Configuration Reference: Single-Cell HDF5 Transformation

> **Related documentation:** [About SC HDF5 Transformations](about-sc-hdf5-transformations.md) · [How-to Guides](how-to-sc-hdf5-transformations.md) · [API Reference](api-reference.md) · [Transformation Process Reference](transformation-process-reference.md)

---

## Quick reference

| Section | Parameter | Type | Required | Default |
|---------|-----------|------|----------|---------|
| *(top-level)* | `file_type` | string | **Yes** | — |
| *(top-level)* | `dry_run` | boolean | No | `false` |
| *(top-level)* | `save_logs` | boolean | No | `true` |
| `biosample_metadata` | `metadata_keys` | dict[str, str] | Yes* | — |
| `biosample_metadata` | `biosample_column_name` | string | Yes* | — |
| `biosample_metadata.sample` | `create_new_group` | boolean | No | `false` |
| `biosample_metadata.sample` | `template_id` | string | No | — |
| `biosample_metadata.sample` | `columns_to_export` | list[string] | No | — |
| `biosample_metadata.sample` | `columns_renaming_map` | dict[str, str] | No | — |
| `biosample_metadata.sample` | `columns_to_fill_missing_values` | dict[str, str] | No | — |
| `biosample_metadata.sample` | `columns_to_curate_values` | dict[str, dict[str, str]] | No | — |
| `biosample_metadata.library` | *(same as sample)* + `linking_group` | string | No | — |
| `biosample_metadata.preparation` | *(same as library)* | — | — | — |
| `cell_metadata` | `metadata_keys` | dict[str, str] | Yes* | — |
| `cell_metadata` | `linking_group` | dict[str, …] | No | auto |
| `cell_metadata` | `columns_to_drop` | list[string] | No | — |
| `cell_metadata` | `columns_renaming_map` | dict[str, str] | No | — |
| `cell_metadata` | `columns_to_fill_missing_values` | dict[str, str] | No | — |
| `cell_metadata` | `columns_to_curate_values` | dict[str, dict[str, str]] | No | — |
| `cell_metadata` | `set_column_value` | dict[str, str] | No | — |
| `cell_metadata` | `columns_to_preserve_name` | list[string] | No | — |
| `cell_metadata` | `add_qc_metrics` | boolean | No | `true` |
| `feature_metadata` | `metadata_keys` | dict[str, str] | Yes* | — |
| `feature_metadata` | `columns_to_drop` | list[string] | No | — |
| `feature_metadata` | `columns_renaming_map` | dict[str, str] | No | — |
| `feature_metadata` | `columns_to_fill_missing_values` | dict[str, str] | No | — |
| `feature_metadata` | `columns_to_curate_values` | dict[str, dict[str, str]] | No | — |
| `feature_metadata` | `set_column_value` | dict[str, str] | No | — |
| `feature_metadata` | `columns_to_preserve_name` | list[string] | No | — |
| `feature_metadata` | `map_gene_ids_to_names` | boolean | No | `true` |
| `cell_expression` | `data_class` | string | **Yes*** | — |
| `cell_expression` | `compression_level` | integer (0–9) | No | `4` |
| `cell_expression` | `chunk_size` | integer | No | auto |
| `cell_expression` | `max_buffer_size` | integer | No | `50` |
| `cell_expression` | `number_format` | string | No | inferred |
| `cell_expression` | `columns_to_drop` | list[string] | No | — |
| `cell_expression` | `columns_renaming_map` | dict[str, str] | No | — |
| `cell_expression` | `set_column_value` | dict[str, str] | No | — |
| `cell_expression` | `source_file_metadata` | boolean | No | `true` |

*Yes* = required only if the parent section is present.

---

## Parameter details

### Top-level

#### `file_type`
Format of the input HDF5 file. Must be provided; the pipeline cannot proceed without a valid file type.
- Accepted values: `"h5ad"`, `"h5"`

#### `dry_run`
Runs all extraction, validation, and linking resolution steps without uploading data or saving logs. Compression is also skipped. Use to validate configuration before committing data.

#### `save_logs`
When `false`, logs are not saved as an attachment after the run. Has no effect when `dry_run` is `true`.

---

### `biosample_metadata`

Settings for extracting, transforming, and exporting cell-level metadata to Sample, Library, or Preparation entities. The entire section is optional.

#### `metadata_keys`
Maps HDF5 group keys to metadata types. Use `"obs": "metadata"` to read standard cell metadata as the source for biosample-level aggregation.

```json
{ "obs": "metadata" }
```

#### `biosample_column_name`
Column identifying which biosample each cell belongs to (e.g. a sample ID or library ID column). Rows are grouped by this column for aggregation.

---

#### `biosample_metadata.sample`

#### `create_new_group`
When `true`, creates a new Sample group in ODM and links it to the study. When `false` or omitted, existing Sample group objects are updated instead.

#### `template_id`
Template ID for the new Sample group. Falls back to the study default if omitted.

#### `columns_to_export`
Cell metadata columns to include in the exported Sample metadata. Only columns that are constant per biosample are eligible; exported columns are automatically dropped from cell metadata.

#### `columns_renaming_map`
Maps source column names to new names.
```json
{ "tissue_type": "tissueType" }
```

#### `columns_to_fill_missing_values`
Default values for missing entries.
```json
{ "disease": "unknown" }
```

#### `columns_to_curate_values`
Replacement values for specific entries in specified columns.
```json
{ "tissue": { "PBMCs": "peripheral blood mononuclear cells" } }
```

---

#### `biosample_metadata.library`

Accepts all parameters from `biosample_metadata.sample`, plus:

#### `linking_group`
Accession of an existing Sample group to link the new Library group to. If omitted, the pipeline uses a Sample group created in the same run, or pre-fetched accessions for the study.

---

#### `biosample_metadata.preparation`

Accepts all parameters from `biosample_metadata.library`, including `linking_group`.

> **Constraint:** Only one of `library` or `preparation` may have `columns_to_export` set in the same configuration.

---

### `cell_metadata`

Settings for extracting and transforming cell-level metadata. Optional. If absent, no Cell Group is created.

#### `metadata_keys`
Maps HDF5 group keys to metadata types. At least one key with value `"metadata"` is required.

| Key | Value | Description |
|-----|-------|-------------|
| `obs` | `metadata` | Standard cell annotations |
| `obsm` | `embedding` | Multidimensional cell data (PCA, UMAP, etc.) |
| `obsp` | `pairwise` | Pairwise cell annotations |

For H5 files, use the same H5AD key names — the transformation maps them to the correct internal structure.

```json
{ "obs": "metadata", "obsm": "embedding", "obsp": "pairwise" }
```

#### `linking_group`
Specifies the parent SLP entity (sample/library/preparation) to link the Cell Group to. Must contain exactly one key. An empty value triggers auto-discovery of all available accessions of that entity type. If absent entirely and no new SLP groups are being created, auto-discovery applies: Library → Preparation → Sample.

```json
{ "library": "GSF017080" }
{ "preparation": [] }
```

#### `columns_to_drop`
Column names to remove before processing.
```json
["taxon", "organism_id"]
```

#### `columns_renaming_map`
Maps source column names to new names.
```json
{ "sample": "batch", "pctmt": "percentMito" }
```

#### `columns_to_fill_missing_values`
Default values for missing entries.
```json
{ "batch": "unknown" }
```

#### `columns_to_curate_values`
Replacement values for specific entries in specified columns.
```json
{ "sample": { "LGVXCTRL1": "lung_healthy_1" } }
```

#### `set_column_value`
Sets a constant value for all rows. Can add new attribute columns or overwrite existing ones.
```json
{ "sample_id": "lung_1" }
```

#### `columns_to_preserve_name`
Columns to exempt from internal name standardisation. Use for column names that contain characters that would otherwise be altered (e.g. Leiden cluster columns: `cluster_leiden_0.5`).
```json
["cluster_leiden_0.5"]
```

#### `add_qc_metrics`
When `true`, QC metrics are calculated and added to cell metadata if not already present: number of counts, number of genes, mitochondrial and ribosomal gene presence. Skipped when `dry_run` is `true`.

---

### `feature_metadata`

Settings for extracting and transforming feature (gene)-level metadata. Optional.

#### `metadata_keys`
Maps HDF5 group keys to metadata types. At least one key with value `"metadata"` is required.

| Key | Value | Description |
|-----|-------|-------------|
| `var` | `metadata` | Standard feature annotations |
| `varm` | `embedding` | Multidimensional feature data |
| `varp` | `pairwise` | Pairwise feature annotations |

For H5 files, use the same H5AD key names.

#### `columns_to_drop`
Column names to remove from feature metadata.

#### `columns_renaming_map`
Maps source column names to new names.

#### `columns_to_fill_missing_values`
Default values for missing entries.

#### `columns_to_curate_values`
Replacement values for specific entries.

#### `set_column_value`
Sets a constant value for all rows.

#### `columns_to_preserve_name`
Columns to exempt from internal name standardisation.

#### `map_gene_ids_to_names`
When `true`, attempts to map gene IDs to gene names if names are absent and the `geneId` column is present. The pipeline infers the ID source (Ensembl or NCBI) and species automatically. Set to `false` for proteomics or other omics data that do not use gene IDs as identifiers.

> The gene ID column must be named `geneId` for mapping to be performed.

Supported organisms (hdf5-cells v0.0.4):

| Organism | Genome version | Ensembl release | NCBI release |
|----------|---------------|-----------------|--------------|
| *Homo sapiens* | GRCh38.p14 | 115 | GCF_000001405.40-RS_2025_08 |
| *Mus musculus* | GRCm39 | 115 | GCF_000001635.27-RS_2024_02 |
| *Rattus norvegicus* | GRCr8 | 115 | GCF_036323735.1-RS_2024_02 |
| *Sus scrofa* | Sscrofa11.1 | 115 | 106 |

---

### `cell_expression`

Settings for extracting and uploading the cell expression matrix. Optional. If absent, no Expression Group is created.

#### `data_class`
Data class label for the expression data.
```json
"Single-cell transcriptomics"
```

#### `compression_level`
Brotli compression level for the output file. Higher values produce smaller files at the cost of longer compression time. Range: 0–9.

#### `chunk_size`
Number of features processed per chunk during export. Calculated automatically from available container memory if omitted.

#### `max_buffer_size`
Amount of data held in memory before being flushed to disk during expression writing.

#### `number_format`
Numeric precision of values in the output file. Accepts printf-style (`"%.7g"`, `"%d"`) or NumPy dtype (`"float32"`, `"int64"`). Inferred from the data if omitted.

#### `columns_to_drop`
Column names to remove from expression metadata.

#### `columns_renaming_map`
Maps source column names to new names in expression metadata.

#### `set_column_value`
Sets a constant value for all rows in specified expression metadata columns.

#### `source_file_metadata`
When `true`, metadata from the source HDF5 attachment is read and included in expression metadata (subject to `columns_to_drop`, `columns_renaming_map`, and `set_column_value`). When `false`, source file metadata extraction is skipped.

Summary statistics are always appended regardless of this flag: total cells, total features, sparsity (%), non-zero values, source file accession, and source file name.
