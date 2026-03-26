# Configuration Reference: Single-Cell HDF5 Transformation

> **Related documentation:** [About SC HDF5 Transformations](about-sc-hdf5-transformations.md) · [How-to Guides](how-to-sc-hdf5-transformations.md) · [API Reference](api-reference.md) · [Transformation Process Reference](transformation-process-reference.md)

The configuration file controls how the transformation reads, processes, and indexes cell and feature metadata from HDF5 files. Parameters are organised by top-level section. The configuration is validated at run start; `file_type` errors fail immediately, all others are reported together at the end of validation. Unrecognised keys are ignored with a warning.

---

## Top-level parameters

**`file_type`** *(string, mandatory)* — Format of the input HDF5 file. Accepted values: `"h5ad"`, `"h5"`.

**`dry_run`** *(boolean, optional, default: `false`)* — When `true`, performs all extraction, validation, and linking resolution without uploading data or saving logs. Compression is also skipped. Use to validate configuration before committing data.

**`save_logs`** *(boolean, optional, default: `true`)* — When `false`, logs are not saved as an attachment after the run. Has no effect when `dry_run` is `true`.

---

## `biosample_metadata`

Settings for extracting, transforming, and exporting cell-level metadata to Sample, Library, or Preparation entities. The entire section is optional.

**`metadata_keys`** *(dict[string, string], mandatory if section is present)* — Maps HDF5 group keys to metadata types. Use `"obs": "metadata"` to read standard cell metadata as the source for biosample-level aggregation. Example:
```json
{ "obs": "metadata" }
```

**`biosample_column_name`** *(string, mandatory if section is present)* — Column identifying which biosample each cell belongs to (e.g. a sample ID or library ID column). Rows are grouped by this column for aggregation.

### sample

Settings for exporting metadata to the Sample entity. Optional.

**`create_new_group`** *(boolean, optional)* — When `true`, creates a new Sample group in ODM and links it to the study. When omitted or `false`, existing Sample group objects are updated instead.

**`template_id`** *(string, optional)* — Template ID for the new Sample group. Falls back to the study default if omitted.

**`columns_to_export`** *(list[string], optional)* — Cell metadata columns to include in the exported Sample metadata. Only columns constant per biosample are eligible; exported columns are automatically dropped from cell metadata.

**`columns_renaming_map`** *(dict[string, string], optional)* — Maps source column names to new names. Example: `{ "tissue_type": "tissueType" }`

**`columns_to_fill_missing_values`** *(dict[string, string], optional)* — Default values for missing entries. Example: `{ "disease": "unknown" }`

**`columns_to_curate_values`** *(dict[string, dict[string, string]], optional)* — Replacement values for specific entries in specified columns. Example:
```json
{ "tissue": { "PBMCs": "peripheral blood mononuclear cells" } }
```

### library

Accepts the same parameters as `sample`, plus:

**`linking_group`** *(string, optional)* — Accession of an existing Sample group to link the new Library group to. If omitted, the pipeline uses a Sample group created in the same run, or pre-fetched accessions for the study.

### preparation

Accepts the same parameters as `library`, including `linking_group`.

> **Constraint:** Only one of `library` or `preparation` may have `columns_to_export` set in the same configuration.

---

## `cell_metadata`

Settings for extracting and transforming cell-level metadata. Optional. If absent, no Cell Group is created.

**`metadata_keys`** *(dict[string, string], mandatory if section is present)* — Maps HDF5 group keys to metadata types. At least one key with value `"metadata"` is required. Accepted values for H5AD files:

- `"obs": "metadata"` — Standard cell annotations
- `"obsm": "embedding"` — Multidimensional cell data (PCA, UMAP, etc.)
- `"obsp": "pairwise"` — Pairwise cell annotations (e.g. cell–cell distances)

For H5 files, use the same H5AD key names — the transformation maps them to the correct internal structure regardless of source format. Example:
```json
{ "obs": "metadata", "obsm": "embedding", "obsp": "pairwise" }
```

**`linking_group`** *(dict[string, string | list[string] | null], optional)* — Specifies the parent SLP entity to link the Cell Group to. Must contain exactly one key: `sample`, `library`, or `preparation`. An empty value (`[]`, `""`, or `null`) triggers auto-discovery of all available accessions of that type. If the parameter is absent entirely and no new SLP groups are being created, auto-discovery applies in this order: Library → Preparation → Sample. Examples:
```json
{ "library": "GSF017080" }
{ "preparation": [] }
```

**`columns_to_drop`** *(list[string], optional)* — Column names to remove before processing. Example: `["taxon", "organism_id"]`

**`columns_renaming_map`** *(dict[string, string], optional)* — Maps source column names to new names. Example: `{ "sample": "batch", "pctmt": "percentMito" }`

**`columns_to_fill_missing_values`** *(dict[string, string], optional)* — Default values for missing entries. Example: `{ "batch": "unknown" }`

**`columns_to_curate_values`** *(dict[string, dict[string, string]], optional)* — Replacement values for specific entries. Example: `{ "sample": { "LGVXCTRL1": "lung_healthy_1" } }`

**`set_column_value`** *(dict[string, string], optional)* — Sets a constant value for all rows. Can add new attribute columns or overwrite existing ones. Example: `{ "sample_id": "lung_1" }`

**`columns_to_preserve_name`** *(list[string], optional)* — Columns to exempt from internal name standardisation. Use for columns whose names contain characters that would otherwise be altered (e.g. Leiden cluster columns with decimal suffixes such as `cluster_leiden_0.5`).

**`add_qc_metrics`** *(boolean, optional, default: `true`)* — When `true`, QC metrics are calculated and added to cell metadata if not already present (counts, genes, mitochondrial and ribosomal gene presence). Skipped when `dry_run` is `true`.

---

## `feature_metadata`

Settings for extracting and transforming feature (gene)-level metadata. Optional.

**`metadata_keys`** *(dict[string, string], mandatory if section is present)* — Maps HDF5 group keys to metadata types. At least one key with value `"metadata"` is required. Accepted values for H5AD files:

- `"var": "metadata"` — Standard feature annotations
- `"varm": "embedding"` — Multidimensional feature data
- `"varp": "pairwise"` — Pairwise feature annotations

For H5 files, use the same H5AD key names. Example: `{ "var": "metadata", "varm": "embedding" }`

**`columns_to_drop`** *(list[string], optional)* — Column names to remove from feature metadata.

**`columns_renaming_map`** *(dict[string, string], optional)* — Maps source column names to new names.

**`columns_to_fill_missing_values`** *(dict[string, string], optional)* — Default values for missing entries.

**`columns_to_curate_values`** *(dict[string, dict[string, string]], optional)* — Replacement values for specific entries.

**`set_column_value`** *(dict[string, string], optional)* — Sets a constant value for all rows.

**`columns_to_preserve_name`** *(list[string], optional)* — Columns to exempt from internal name standardisation.

**`map_gene_ids_to_names`** *(boolean, optional, default: `true`)* — When `true`, attempts to map gene IDs to gene names if names are absent and the `geneId` column is present. The pipeline infers the ID source (Ensembl or NCBI) and species automatically. Set to `false` for proteomics or other omics data that do not use gene IDs as identifiers.

> The gene ID column must be named `geneId` for mapping to be performed.

Supported organisms (hdf5-cells v0.0.4): *Homo sapiens* (GRCh38.p14, Ensembl 115), *Mus musculus* (GRCm39, Ensembl 115), *Rattus norvegicus* (GRCr8, Ensembl 115), *Sus scrofa* (Sscrofa11.1, Ensembl 115).

---

## `cell_expression`

Settings for extracting and uploading the cell expression matrix. Optional. If absent, no Expression Group is created.

**`data_class`** *(string, mandatory if section is present)* — Data class label for the expression data. Example: `"Single-cell transcriptomics"`

**`compression_level`** *(integer 0–9, optional, default: `4`)* — Brotli compression level for the output file. Higher values produce smaller files at the cost of longer compression time.

**`chunk_size`** *(integer, optional)* — Number of features processed per chunk during export. Calculated automatically from available container memory if omitted.

**`max_buffer_size`** *(integer, optional, default: `50`)* — Amount of data held in memory before being flushed to disk during expression writing.

**`number_format`** *(string, optional)* — Numeric precision of values in the output file. Accepts printf-style (`"%.7g"`, `"%d"`) or NumPy dtype (`"float32"`, `"int64"`). Inferred from the data if omitted.

**`columns_to_drop`** *(list[string], optional)* — Column names to remove from expression metadata.

**`columns_renaming_map`** *(dict[string, string], optional)* — Maps source column names to new names in expression metadata.

**`set_column_value`** *(dict[string, string], optional)* — Sets a constant value for all rows in specified expression metadata columns.

**`source_file_metadata`** *(boolean, optional, default: `true`)* — When `true`, metadata from the source HDF5 attachment is read and included in expression metadata (subject to `columns_to_drop`, `columns_renaming_map`, and `set_column_value`). When `false`, source file metadata extraction is skipped. In all cases, summary statistics are always appended (total cells, total features, sparsity %, non-zero values, source file accession and name).
