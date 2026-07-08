# Transformation process reference: Single-cell HDF5 transformation

This reference describes the internal processing stages of the single-cell HDF5 transformation pipeline. It is intended for users who need to understand what the pipeline does at each stage: for example, to interpret logs, diagnose errors, or reason about the order of operations.

For related documentation: [About single-cell transformations](about-single-cell-transformations.md) · [Configuration reference](configuration-reference.md) · [Getting started](single-cell-getting-started.md)

---

## Stage 1: Initial setup and file preparation

### 1.1 Configuration loading and validation

The pipeline reads the transformation configuration and validates all fields. The configuration version that was loaded is recorded in the log.

Top-level key validation checks the presence and data types of `file_type`, `biosample_metadata`, `cell_metadata`, `feature_metadata`, and `cell_expression`. If `file_type` is missing or contains an unsupported value (`"h5ad"` and `"h5"` are the only accepted values), the pipeline raises an error immediately.

For all remaining sections, validation errors are accumulated and reported together at the end of the validation stage, so all issues are surfaced in a single run.

Per-section validation covers: presence of required keys, data type correctness, key-value correctness for `metadata_keys` entries. `biosample_metadata` validation ensures that `library` and `preparation` are not both configured for simultaneous update. `cell_expression` validation resolves `number_format` to a dtype stored for downstream use. Unrecognised keys are logged as warnings and ignored.

### 1.2 Attachment and study metadata retrieval

The pipeline retrieves the accession and metadata of the input HDF5 attachment from ODM to determine the name to assign to the processed data objects and the study accession to which the resulting Cell Group and Expression Group will be associated.

### 1.3 Linking group determination

Before any file processing begins, the pipeline resolves the parent SLP entity (Sample, Library, or Preparation group) to link the Cell Group to. The resolution follows these rules in order:

- **New SLP group creation deferred:** If `biosample_metadata` is present and any entity has `create_new_group: true`, linking resolution is deferred until after those new groups are created (Stage 4). Example:

```json
"biosample_metadata": {
  "metadata_keys": { "obs": "metadata" },
  "biosample_column_name": "sample_id",
  "sample": { "create_new_group": true }
}
```

- **Explicit `linking_group`:** If `cell_metadata.linking_group` is set, the specified entity type and accession(s) are used directly. An empty value resolves to all available group accessions of the specified entity type for the study. Examples:

```json
"cell_metadata": { "linking_group": { "sample": ["GSF000001"] } }
```

```json
"cell_metadata": { "linking_group": { "preparation": [] } }
```

- **Auto-discovery:** If neither of the above applies, the pipeline fetches all SLP groups for the study and selects the first entity type that has at least one group, checking in the order Library → Preparation → Sample. All accessions of the selected type are used.

If no SLP group can be found and no new group is being created, the pipeline raises an error.

### 1.4 Temporary directory and file preparation

A temporary directory is created for all intermediate files. The input HDF5 file is copied into this directory. If the input is `"h5"` (10x Genomics H5), it is converted to H5AD format so that subsequent stages can apply unified processing regardless of source format.

### 1.5 File structure inspection

The pipeline opens the H5AD file and logs its structure: top-level keys (groups), data types and shapes, and attribute names. This output is useful for verifying which metadata keys (`obs`, `var`, `obsm`, etc.) are present before extraction begins.

---

## Stage 2: Metadata extraction

Each configured section (`biosample_metadata`, `cell_metadata`, `feature_metadata`) is processed independently.

### 2.1 Configuration and input validation

For each metadata section, the pipeline reads parameters and validates the presence of required keys and supported file types.

### 2.2 Biosample metadata (`biosample_metadata` config)

When `biosample_metadata` is present, the pipeline can export Sample, Library, or Preparation-level attributes derived from cell-level metadata. Only one of `library` or `preparation` may have `columns_to_export` set. Attributes exported to biosample metadata are automatically removed from cell metadata.

**File reading and extraction:** The pipeline opens the H5AD file, reads the metadata from the group indicated by `metadata_keys`, and organises the table by `biosample_column_name`. Only attributes constant within a biosample and listed in `columns_to_export` are processed. The result is written to a TSV file in the temporary directory.

**Discovery mode:** Activated only when `dry_run` is enabled, `biosample_metadata` is present, and no entity has `columns_to_export` defined. The pipeline logs the number of unique biosamples and the attributes constant within each biosample, then exits without writing a TSV. No ODM objects are created or modified.

**Existing biosample metadata update:** When `columns_to_export` is configured for an entity but `create_new_group` is not set, the pipeline prepares an update to existing ODM objects. It fetches current metadata for the entity type, joins extracted metadata to existing metadata by the entity ID column (Sample Source ID, Library ID, or Preparation ID), and retains only attributes not already present in ODM. If any extracted ID does not match an existing ODM object, an error is raised listing the unmatched IDs.

### 2.3 Cell and feature metadata extraction

The pipeline opens the H5AD file and reads groups specified in `metadata_keys`:

- Standard metadata (`"metadata"`) is loaded into a DataFrame.
- Embeddings (`"embedding"`) are read as multidimensional arrays, serialised as comma-separated strings, and added as columns.
- Pairwise data (`"pairwise"`) is read as pairwise matrices; for each matrix, the row mean is calculated and added as a column.

### 2.4 Index handling and sanity checks

- If the DataFrame is empty with neither columns nor an index, an error is raised.
- An unnamed index is assigned the default name `_index`.
- If the index name collides with an existing column name, it is renamed to avoid the conflict.
- The index is extracted and appended as a column so that barcode or feature ID information is preserved.

> If the cell barcode is in the index and the index has no name, the extracted column is named `_index`. `_index` should be renamed to barcode via `columns_renaming_map`.

### 2.5 Column operations

The following transformations are applied in order:

1. Drop columns (`columns_to_drop`)
2. Rename columns (`columns_renaming_map`)
3. Curate values (`columns_to_curate_values`)
4. Fill missing values (`columns_to_fill_missing_values`)
5. Set constant values (`set_column_value`)

After explicit column operations, attribute name standardisation is applied: column names are mapped to ODM canonical names where a mapping exists; non-standard names are converted to camelCase. Columns in `columns_to_preserve_name` are exempt. For the full mapping list, see [Attribute Mapping Reference](attribute-mapping-reference.md).

**Cell metadata additional steps:**

- **Required column validation:** `barcode` (unique cell identifiers, duplicates or missing values cause an error) and `batch` (SLP linking identifiers, missing values cause an error).
- **QC metric calculation:** number of counts, number of genes, percentage mitochondrial expression, and percentage ribosomal expression are added if not already present. Skipped when `add_qc_metrics: false` or when `dry_run: true`.

**Feature metadata additional steps:**

- **Gene ID mapping:** If gene names are absent and the `geneId` column is present, the pipeline infers the ID source (Ensembl or NCBI) and species, then adds a gene names column. The step can be skipped with `map_gene_ids_to_names: false`. For more details , see [Attribute Mapping Reference](attribute-mapping-reference.md#gene-id-to-name-mapping).

### 2.6 Storing data

The processed metadata DataFrame is written to the temporary directory as a TSV file.

---

## Stage 3: Cell expression extraction

### 3.1 Configuration and input validation

The pipeline reads expression parameters: `data_class`, `compression_level`, `chunk_size`, `max_buffer_size`, and `number_format`. Parameters not specified in the configuration are inferred from the data or set to sensible defaults.

### 3.2 Expression matrix reading and validation

The cell expression matrix is read from the HDF5 file. The pipeline validates that the matrix shape matches the number of cells and features determined in Stage 2.

### 3.3 Expression data writing

The expression data, enriched with feature metadata according to the configuration, is written to a Brotli-compressed file (`.br`) in the temporary directory.

### 3.4 Expression metadata reading and writing

Expression metadata from the source attachment is read and transformed according to `columns_to_drop`, `columns_renaming_map`, and `set_column_value`, unless `source_file_metadata` is `false`.

The following statistics are always computed and appended regardless of the `source_file_metadata` flag:

1. Total Number of Cells or Nuclei
2. Total Number of Features
3. Sparsity Percentage Value
4. Number of Non-zero Values
5. Source File Accession
6. Source File Name
7. Transformation Job ID

---

## Stage 4: Final steps and upload

### 4.1 Dry run exit

If `dry_run: true`, the pipeline performs linking validation and exits at this point. Expression matrix compression is skipped. Logs are reported and available in the API.

Best-effort linking validation:

- **Biosample coverage:** Unique values in the cell metadata `batch` column are compared against ID values of the resolved SLP groups. Unmatched values are logged as warnings.
- **Duplicate IDs:** If the same ID value appears in more than one SLP object, a warning is logged.
- **Group accession coverage:** Group accessions containing no biosample objects matching any cell `batch` value are logged as warnings.

Validation mismatches are reported as warnings and do not abort the dry run.

### 4.2 Upload to ODM

#### 4.2.1 SLP groups

If `biosample_metadata` is configured with at least one entity:

- **New groups** (`create_new_group: true`): The corresponding TSV is uploaded as a new group via the entity-specific API endpoint with `template_id` applied if specified. Sample Groups are linked to the study; Library and Preparation Groups are linked to a Sample Group resolved by checking `linking_group.sample` in the entity's configuration, then a Sample Group created in the same run, then pre-fetched Sample Group accessions. The new group accession is stored for use in the cell group linking step.
- **Existing groups** (`create_new_group` not set): For each row in the update TSV, the pipeline updates the corresponding object via the ODM PATCH API endpoint.

#### 4.2.2 Cell Group upload

The transformed cell metadata TSV is uploaded as a new Cell Group, linked to the parent SLP Groups determined in Stage 1.3 or Stage 4.2.1.

#### 4.2.3 Expression Group upload

The Brotli-compressed expression file and its metadata file are uploaded to create a new Expression Group, linked to the newly created Cell Group.

