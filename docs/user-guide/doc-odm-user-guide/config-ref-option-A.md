# Configuration Reference: Single-Cell HDF5 Transformation

> **Related documentation:** [About SC HDF5 Transformations](about-sc-hdf5-transformations.md) · [How-to Guides](how-to-sc-hdf5-transformations.md) · [API Reference](api-reference.md) · [Transformation Process Reference](transformation-process-reference.md)

The configuration is validated at the start of every run. If `file_type` is missing or invalid, the pipeline raises an error immediately. All other validation errors are collected and reported together. Unrecognised keys are ignored with a warning.

---

## Top-level parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_type` | `string` | **Yes** | — | Format of the input file. Accepted values: `"h5ad"`, `"h5"`. |
| `save_logs` | `boolean` | No | `true` | When `false`, logs are not saved as an attachment after the run. Has no effect when environment variable `dry_run` is `true`. |

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
| `linking_group` | `dict[string, string \| list[string] \| null]` | No | — | Specifies the parent SLP entity (sample/library/preparation) to link the Cell Group to. Empty value triggers auto-discovery of all available accessions. |
| `columns_to_drop` | `list[string]` | No | — | Column names to remove before processing. |
| `columns_renaming_map` | `dict[string, string]` | No | — | Maps source column names to new names. |
| `columns_to_fill_missing_values` | `dict[string, string]` | No | — | Default values for missing entries. |
| `columns_to_curate_values` | `dict[string, dict[string, string]]` | No | — | Replacement values for specific entries in specified columns. |
| `set_column_value` | `dict[string, string]` | No | — | Sets a constant value for all rows. Can add new columns or overwrite existing ones. |
| `columns_to_preserve_name` | `list[string]` | No | — | Columns to exempt from internal name standardisation (e.g. Leiden cluster columns with decimal suffixes). |
| `add_qc_metrics` | `boolean` | No | `true` | When `true`, adds QC metrics (counts, genes, mitochondrial/ribosomal presence) if not already present. Skipped when environment variable `dry_run` is `true`. |

**`metadata_keys` accepted values (H5AD):**

| Key | Value | Description |
|-----|-------|-------------|
| `obs` | `metadata` | Standard cell annotations |
| `obsm` | `embedding` | Multidimensional cell data (PCA, UMAP, etc.) |
| `obsp` | `pairwise` | Pairwise cell annotations |

For H5 files, use the same H5AD key names — the transformation maps them to the correct internal structure.

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

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `metadata_keys` | `dict[string, string]` | Yes | — | Maps HDF5 group keys to metadata types. At least one key with value `"metadata"` is required. |
| `columns_to_drop` | `list[string]` | No | — | Column names to remove from feature metadata. |
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

> The gene ID column must be named `geneId` for mapping to be performed.

**Supported organisms (`map_gene_ids_to_names`) — hdf5-cells v0.0.4:**

| Organism | Genome version | Ensembl release | NCBI release |
|----------|---------------|-----------------|--------------|
| *Homo sapiens* | GRCh38.p14 | 115 | GCF_000001405.40-RS_2025_08 |
| *Mus musculus* | GRCm39 | 115 | GCF_000001635.27-RS_2024_02 |
| *Rattus norvegicus* | GRCr8 | 115 | GCF_036323735.1-RS_2024_02 |
| *Sus scrofa* | Sscrofa11.1 | 115 | 106 |

---

## `cell_expression`

Settings for extracting and uploading the cell expression matrix. Optional. If absent, no Expression Group is created.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `data_class` | `string` | **Yes** | — | Data class label for the expression data (e.g. `"Single-cell transcriptomics"`). |
| `compression_level` | `integer` (0–9) | No | `4` | Brotli compression level. Higher values produce smaller files at the cost of longer compression time. |
| `chunk_size` | `integer` | No | auto | Number of features processed per chunk. Calculated automatically from available memory if omitted. |
| `max_buffer_size` | `integer` | No | `50` | Amount of data held in memory before being flushed to disk during writing. |
| `number_format` | `string` | No | inferred | Numeric precision of output values. Accepts printf-style (`"%.7g"`, `"%d"`) or NumPy dtype (`"float32"`, `"int64"`). |
| `columns_to_drop` | `list[string]` | No | — | Column names to remove from expression metadata. |
| `columns_renaming_map` | `dict[string, string]` | No | — | Maps source column names to new names. |
| `set_column_value` | `dict[string, string]` | No | — | Sets a constant value for all rows in specified columns. |
| `source_file_metadata` | `boolean` | No | `true` | When `true`, metadata from the source HDF5 attachment is read and included in expression metadata. Summary statistics (cell count, feature count, sparsity, etc.) are always appended regardless of this flag. |
