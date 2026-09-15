---
diataxis: reference
tab: odm-api
---

# Configuration reference: Single-cell HDF5 transformation

The configuration is validated at the start of every run. If `file_type` is missing or invalid, the pipeline raises an error immediately. All other validation errors are collected and reported together. Unrecognised keys are ignored with a warning.

For related documentation: [About single-cell transformations](about-single-cell-transformations.md) · [How-to guides](ingest-cell-and-expression.md) · [API reference](/swagger/?urls.primaryName=processorsController) · [Transformation process reference](transformation-process-reference.md)

---

## Top-level parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_type` | `string` | **Yes** | — | Format of the input file. Accepted values: `"h5ad"`, `"h5"`. |

---

## `biosample_metadata`

Settings for extracting, transforming, and exporting cell-level metadata to Sample, Library, or Preparation entities. The entire section is optional.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `metadata_keys` | `dict[string, string]` | Yes | — | Maps HDF5 group keys to metadata types. Use `"obs": "metadata"` to read standard cell metadata. |
| `biosample_column_name` | `string` | Yes | — | Column identifying which biosample each cell belongs to. Rows are grouped by this column for aggregation. |

**`metadata_keys` example:**

```json
{ "obs": "metadata" }
```

### `biosample_metadata.sample`

Settings for exporting metadata to the Sample entity. Optional.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `create_new_group` | `boolean` | `false` | When `true`, creates a new Sample group in ODM and links it to the study. |
| `template_id` | `string` | — | Template ID for the new Sample group. Falls back to the study default if omitted. |
| `columns_to_export` | `list[string]` | — | Cell metadata columns to include in the exported Sample metadata. Only columns constant per biosample are eligible; exported columns are dropped from cell metadata. |
| `copy_columns_map` | `dict[string, string]` | — | Copies values from a source column into a destination column, before renaming. Maps source name to destination name. |
| `columns_renaming_map` | `dict[string, string]` | — | Maps source column names to new names in the exported metadata. |
| `columns_to_fill_missing_values` | `dict[string, string]` | — | Default values for missing entries in specified columns. |
| `columns_to_curate_values` | `dict[string, dict[string, string]]` | — | Maps specific values in a column to replacement values. |

**Examples:**

```json
{ "columns_renaming_map": { "tissue_type": "tissueType" } }
{ "columns_to_fill_missing_values": { "disease": "unknown" } }
{ "columns_to_curate_values": { "tissue": { "PBMCs": "peripheral blood mononuclear cells" } } }
```

### `biosample_metadata.library`

Accepts the same parameters as `biosample_metadata.sample`, plus:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `linking_group` | `string` | — | Accession of an existing Sample group to link the new Library group to. If omitted, the pipeline uses a Sample group from the same run or pre-fetched accessions. |

### `biosample_metadata.preparation`

Accepts the same parameters as `biosample_metadata.library`, including `linking_group`.

> **Constraint:** Only one of `library` or `preparation` may have `columns_to_export` set in the same configuration.

---

## `cell_metadata`

Settings for extracting and transforming cell-level metadata. Optional. If absent, no Cell Group is created.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `metadata_keys` | `dict[string, string]` | Yes | — | Maps HDF5 group keys to metadata types. At least one key with value `"metadata"` is required. |
| `linking_group` | `dict[string, string \| list[string] \| null]` | No | — | Specifies the parent SLP entity (`sample`, `library` or `preparation`) to link the Cell Group to. Empty value triggers auto-discovery of all available accessions. For full linking resolution rules, see [Linking group determination](transformation-process-reference.md#13-linking-group-determination). |
| `columns_to_drop` | `list[string]` | No | — | Column names to remove before processing. |
| `copy_columns_map` | `dict[string, string]` | No | — | Copies values from a source column into a destination column. Maps source name to destination name. The destination may be a new column or an existing one, which is overwritten. |
| `columns_renaming_map` | `dict[string, string]` | No | — | Maps source column names to new names. |
| `columns_to_fill_missing_values` | `dict[string, string]` | No | — | Default values for missing entries. |
| `columns_to_curate_values` | `dict[string, dict[string, string]]` | No | — | Replacement values for specific entries in specified columns. |
| `set_column_value` | `dict[string, string]` | No | — | Sets a constant value for all rows. Can add new columns or overwrite existing ones. |
| `columns_to_preserve_name` | `list[string]` | No | — | Columns to exempt from internal name standardisation (e.g. Leiden cluster columns with decimal suffixes). |
| `add_qc_metrics` | `boolean` | No | `true` | When `true`, adds QC metrics (counts, genes, mitochondrial/ribosomal presence) if not already present. Skipped when the job is submitted with `dry_run: true`. |

**`metadata_keys` accepted values (H5AD):**

| Key | Value | Description |
|-----|-------|-------------|
| `obs` | `metadata` | Standard cell annotations |
| `obsm` | `embedding` | Multidimensional cell data (PCA, UMAP, etc.) |
| `obsp` | `pairwise` | Pairwise cell annotations |

For H5 files, use the same H5AD key names: the transformation maps them to the correct internal structure.

**Examples:**

```json
{ "metadata_keys": { "obs": "metadata", "obsm": "embedding" } }
{ "linking_group": { "library": "GSF017080" } }
{ "columns_to_drop": ["taxon", "organism_id"] }
{ "columns_renaming_map": { "sample": "batch", "pctmt": "percentMito" } }
{ "set_column_value": { "sample_id": "lung_1" } }
{ "columns_to_preserve_name": ["cluster_leiden_0.5"] }
```

---

## `feature_metadata`

Settings for extracting and transforming feature (gene)-level metadata. Optional.

If you extract a matrix whose features come from a different source than default `X`'s (`.raw`, for example), see [Configuring features per matrix source](#configuring-features-per-matrix-source) below.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `metadata_keys` | `dict[string, string]` | Yes | — | Maps HDF5 group keys to metadata types. At least one key with value `"metadata"` is required. |
| `columns_to_drop` | `list[string]` | No | — | Column names to remove from feature metadata. |
| `copy_columns_map` | `dict[string, string]` | No | — | Copies values from a source column into a destination column. Maps source name to destination name. The destination may be a new column or an existing one, which is overwritten. |
| `columns_renaming_map` | `dict[string, string]` | No | — | Maps source column names to new names. |
| `columns_to_fill_missing_values` | `dict[string, string]` | No | — | Default values for missing entries. |
| `columns_to_curate_values` | `dict[string, dict[string, string]]` | No | — | Replacement values for specific entries. |
| `set_column_value` | `dict[string, string]` | No | — | Sets a constant value for all rows. |
| `columns_to_preserve_name` | `list[string]` | No | — | Columns to exempt from internal name standardisation. |
| `map_gene_ids_to_names` | `boolean` | No | `true` | When `true`, maps gene IDs to gene names if names are absent and `geneId` column is present. Set to `false` for proteomics or non-gene-ID data. |

**`metadata_keys` accepted values (H5AD):**

| Key | Value | Description |
|-----|-------|-------------|
| `var` | `metadata` | Standard feature annotations |
| `varm` | `embedding` | Multidimensional feature data |
| `varp` | `pairwise` | Pairwise feature annotations |

### Configuring features per matrix source

The parameters above configure the features of root matrix `X` and of every matrix in the `.layers` group, which all share one feature table. A matrix held elsewhere in the file has its own feature table instead, so a configuration extracting such a matrix says which settings belong to which source. The section then takes a prefixed (`/` or `.`) keyed form, one entry per source, key being the path of the object that holds the features:

```json
"feature_metadata": {
  "/raw": {
    "metadata_keys": { "var": "metadata" }
  }
}
```

| Key | Configures the features of |
|-----|----------------------------|
| `/` | `/X` and every `/layers/...` matrix |
| `/raw` | `/raw/X`, which holds its own feature table (typically more features than `/X`, since `/raw` is pre-filtering) |

Each entry accepts the same parameters as the plain form, and `metadata_keys` is written relative to its source, so `"var"` inside `/raw` means `/raw/var` path to the feature table.

**A section is either plain settings or keyed entries, not both.** Leaving a parameter such as `metadata_keys` beside a keyed entry is a configuration error, because it does not say which source the parameter belongs to.

Every extracted matrix must have its source configured. Settings are never applied to a source they were not written for: renaming and gene-ID mapping intended for one feature table can produce misleading labels on another.

To configure a source without any column rules, use `{}`. Its matrix is then labelled by feature name only, with no feature attributes; if that table does hold columns, the job logs a warning naming them, so nothing is dropped unnoticed.

Omitting `feature_metadata` entirely is also valid: every matrix is then labelled by feature name from the `var` of its own source, with no feature attributes.

---

## `cell_expression`

Settings for extracting and uploading the cell expression matrix. Optional. If absent, no Expression Group is created.

By default the transformation extracts root matrix `X`. To extract a different matrix, see [Extracting a matrix other than default X](#extracting-a-matrix-other-than-default-x) below.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data_class` | `string` | **Yes** | — | Data class label for the expression data (e.g. `"Single-cell transcriptomics"`). |
| `compression_level` | `integer` (0–9) | No | `4` | Brotli compression level. Higher values produce smaller files at the cost of longer compression time. |
| `chunk_size` | `integer` | No | inferred | Number of features processed per chunk. Calculated automatically from available memory if omitted. |
| `max_buffer_size` | `integer` | No | `50` | Amount of data (in MB) held in memory before being flushed to disk during writing. |
| `number_format` | `string` | No | inferred | Numeric precision of output values. Accepts printf-style (`"%.7g"`, `"%d"`) or NumPy dtype (`"float32"`, `"int64"`). An integer format is accepted on a matrix stored as floating point when its values are whole numbers; a matrix containing fractional values is rejected rather than truncated. |
| `columns_to_drop` | `list[string]` | No | — | Column names to remove from expression metadata. |
| `columns_renaming_map` | `dict[string, string]` | No | — | Maps source column names to new names. |
| `set_column_value` | `dict[string, string]` | No | — | Sets a constant value for all rows in specified columns. |
| `source_file_metadata` | `boolean` | No | `true` | When `true`, metadata from the source HDF5 attachment is read and included in expression metadata. Summary statistics (cell count, feature count, sparsity, etc.) are always appended regardless of this flag. |

An unrecognised key in `cell_expression` is a configuration error.

### Extracting a matrix other than default `X`

A key beginning with `/` names a matrix in the source file; every other key is a setting. `.` is accepted in place of `/`. Naming the same matrix twice, in whichever spelling, is a configuration error.

```json
"cell_expression": {
  "/layers/lognorm": { "data_class": "Single-cell transcriptomics", "number_format": "%.7g" }
}
```

| Entry | Matrix extracted |
|-------|------------------|
| *(no matrix keys)* | `/X`, the default |
| `/X` | the root matrix `X` |
| `/raw/X` | the `X` matrix inside `.raw` |
| `/layers/lognorm` | the layer named `lognorm` |
| `/layers/raw` | the layer named `raw`, as distinct from `/raw/X` |

A matrix key takes an optional block of settings. Any parameter from the table above may be given at the top level of `cell_expression`, where it applies to every matrix extracted, or inside a matrix's own block, where it applies to that matrix alone; a block takes precedence. `data_class` must be resolvable for each matrix, from its own block or from a top-level value.

If the matrix's features come from a different source than `/X`'s, configure that source as well. See [`feature_metadata`](#feature_metadata).

> **Note:** Currently a Cell Group can be linked to a single Expression Group, so configure one matrix per job and run further matrices as separate jobs. A configuration naming several matrices is rejected during validation, before any data is read.
