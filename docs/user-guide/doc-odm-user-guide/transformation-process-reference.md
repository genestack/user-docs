# Transformation Process Reference: Single-Cell HDF5 Transformation

> **Related documentation:** For conceptual background, see [About Single-Cell HDF5 Transformations in ODM](about-sc-hdf5-transformations.md). For configuration parameter definitions and default values, see the [Configuration Reference](configuration-reference.md).

This reference describes the internal processing stages of the single-cell HDF5 transformation pipeline. It is intended for users who need to understand what the pipeline does at each stage — for example, to interpret logs, diagnose errors, or reason about the order of operations. It is not a guide to running the transformation; see the [How-to Guides](how-to-sc-hdf5-transformations.md) for that purpose.

---

## Stage 1: Initial setup and file preparation

### 1.1 Configuration loading and validation

The pipeline reads the transformation configuration file and validates all fields.

**Top-level key validation** is performed first, checking the presence and data types of: `file_type`, `save_logs`, `biosample_metadata`, `cell_metadata`, `feature_metadata`, and `cell_expression`. If `file_type` is missing or contains an unsupported value (`"h5ad"` and `"h5"` are the only accepted values), the pipeline raises an error immediately and does not proceed.

For all remaining sections, validation errors are accumulated and reported together at the end of the validation stage, so that all issues in the configuration are surfaced in a single run.

**Per-section validation** covers:

- Presence of required keys within each optional section.
- Data type correctness for every key in the section.
- Key-value correctness for `metadata_keys` entries.
- `biosample_metadata`: ensures that `library` and `preparation` are not both configured for simultaneous update.
- `cell_expression`: validates `number_format` as either a printf-format string or a NumPy dtype string; the resolved dtype is stored back into the configuration for downstream use.

Unrecognized keys at any level are logged as warnings and ignored.

### 1.2 Attachment and study metadata retrieval

The pipeline retrieves the accession and metadata of the input HDF5 attachment from ODM. From this, it determines:

- The name to assign to the processed data objects.
- The study accession that the resulting Cell Group and Expression Group will be associated with.

### 1.3 Linking group determination

Before any file processing begins, the pipeline resolves the parent SLP entity (Sample, Library, or Preparation group) to which the Cell Group will be linked. The resolution follows these rules in order:

- **New SLP group creation deferred:** If `biosample_metadata` is present and any of `sample`, `library`, or `preparation` has `create_new_group: true`, linking resolution is deferred until after those new groups are created and uploaded (Stage 4). The cell group is then linked to the newly created groups.

- **Explicit `linking_group` in `cell_metadata`:** If `cell_metadata.linking_group` is set, the specified entity type and accession(s) are used directly. An empty value (e.g. `[]`) resolves to all available group accessions of the specified entity type for the study.

- **Auto-discovery:** If neither of the above applies, the pipeline fetches all SLP groups associated with the study from ODM and selects the first entity type that has at least one group, checking in the order: **Library → Preparation → Sample**. All accessions of the selected type are used for linking.

If no SLP group can be found and no new group is being created, the pipeline raises an error.

### 1.4 Temporary directory and file preparation

A temporary directory is created to store all intermediate files produced during the run. The input HDF5 file is copied into this directory. If the input is of type `"h5"` (10x Genomics H5), it is converted to H5AD format and stored alongside the original copy, so that subsequent stages can stream from the H5AD representation uniformly regardless of source format.

### 1.5 File structure inspection

The pipeline opens the H5AD file and inspects its structure, logging:

- Top-level keys (groups).
- Data types and shapes.
- Attribute names.

This output is written to the transformation logs and is useful for verifying which metadata keys (such as `obs`, `var`, `obsm`) are present in the file before extraction begins.

---

## Stage 2: Metadata extraction

The configuration is checked to determine whether processing for `biosample_metadata`, `cell_metadata`, and/or `feature_metadata` is required. Each configured section is processed independently according to the steps below.

### 2.1 Configuration and input validation

For each metadata section, the pipeline reads parameters (data type, input/output files, file type, metadata keys, column operations) and validates the presence of required keys and supported file types.

### 2.2 Biosample metadata (`biosample_metadata` config)

When `biosample_metadata` is present in the configuration, the pipeline can export Sample, Library, or Preparation-level attributes derived from cell-level metadata.

#### Configuration and input validation

Parameters are read from `biosample_metadata`: `metadata_keys`, `biosample_column_name`, and per-entity settings under `sample`, `library`, and/or `preparation`. These include parameters for identifying exportable attributes (`columns_to_export`), metadata curation (`columns_renaming_map`, `columns_to_fill_missing_values`, `columns_to_curate_values`), and group creation and linking (`create_new_group`, `template_id`, `linking_group`).

Only one of `library` or `preparation` may have `columns_to_export` set. Attributes exported to biosample metadata are automatically removed from the cell metadata in the subsequent processing step. Biosample attributes that do not need to be exported but also should not remain in cell metadata must be listed in `cell_metadata.columns_to_drop`.

#### File reading and metadata extraction

The pipeline opens the H5AD file, reads the metadata from the group indicated by `metadata_keys`, and organizes the resulting table by `biosample_column_name`. Only attributes that are constant within a biosample and listed in `columns_to_export` are processed for export.

For each entity type with `columns_to_export` configured, columns are filtered and optionally curated; the entity ID column(s) (e.g. Sample Source ID, Library ID, Preparation ID) are set from the configuration, and the result is written to a TSV file in the temporary directory.

Exporting a placeholder group containing only ID column(s) can be configured by setting `create_new_group: true` and omitting `columns_to_export`.

#### Discovery mode

Discovery mode is activated only when `dry_run` is enabled, `biosample_metadata` is present, and no entity has `columns_to_export` defined. In this mode, the pipeline logs the number of unique biosamples and the attributes constant within each biosample, then exits without writing a TSV. No ODM objects are created or modified.

#### Existing biosample metadata update

When `columns_to_export` is configured for an entity but `create_new_group` is not set, the pipeline prepares an update to existing ODM metadata objects rather than creating new groups.

It fetches the current metadata for the entity type, then runs a matching procedure joining the extracted metadata to the existing metadata on the entity ID column (e.g. Sample Source ID, Library ID, Preparation ID). Only attributes that do not already exist in the ODM metadata are retained; columns with the same name are skipped. If any extracted ID does not match an existing ODM object, an error is raised listing the unmatched IDs. The matching result is written as a TSV file for use in Stage 4.

### 2.3 File reading and metadata extraction

For cell and feature metadata sections, the pipeline opens the H5AD file and reads the groups specified in `metadata_keys`:

- Standard metadata (value `"metadata"`) is loaded into a DataFrame.
- **Embeddings** (`"embedding"`): Multidimensional arrays are serialized as comma-separated strings and added as columns.
- **Pairwise** (`"pairwise"`): The row mean of each pairwise matrix is calculated and added as a column.

### 2.4 Index handling and sanity checks

- If the DataFrame is empty and has neither columns nor an index, an error is raised.
- If the index is unnamed, it is assigned the default name `_index`.
- If the index name collides with an existing column name, it is renamed to avoid the conflict.
- The index is extracted and appended as a column to ensure barcode or feature ID information is preserved for downstream validation.

> **Note:** If the cell barcode is stored in the index and the index has no name, the extracted column will be named `_index`. To use a different name, rename it using `columns_renaming_map` in the configuration.

### 2.5 Column operations

The following transformations are applied in the order listed, when specified in the configuration:

1. **Drop columns** (`columns_to_drop`)
2. **Rename columns** (`columns_renaming_map`)
3. **Curate values** (`columns_to_curate_values`)
4. **Fill missing values** (`columns_to_fill_missing_values`)
5. **Set constant values** (`set_column_value`)

After all explicit column operations, **attribute name standardization** is applied: column names are mapped to ODM standard attribute names where a mapping exists; non-standard names are converted to camelCase. Columns listed in `columns_to_preserve_name` are exempt from this step. For the full list of recognized column names, see the [Attribute Mapping Reference](attribute-mapping.md). 

Data type validation is then performed on the resulting DataFrame.

**Cell metadata additional steps:**

- **Required column validation:**
  - `barcode`: Unique cell identifiers. Duplicate or missing values cause an error.
  - `batch`: Sample, Library, or Preparation identifiers used for linking. Missing values cause an error.
- **QC metric calculation** (if `add_qc_metrics` is not `false` and environment variable `dry_run` is `false`): Number of counts, number of genes, percentage mitochondrial expression, and percentage ribosomal expression are computed and added if not already present.

**Feature metadata additional steps:**

- **Gene ID mapping** (if `map_gene_ids_to_names` is `true`): If gene names are absent and the standard `geneId` column is present, the pipeline infers the ID source (Ensembl or NCBI) and the species. If both can be determined, a new column with the mapped gene names is added. Supported organisms and annotation releases are listed in [Gene ID to name mapping](attribute-mapping.md#gene-id-to-name-mapping)).

### 2.6 Storing data

The processed metadata DataFrame is written to the temporary directory as a TSV file.

---

## Stage 3: Cell expression extraction

### 3.1 Configuration and input validation

The pipeline reads expression parameters: `data_class`, `compression_level`, `chunk_size`, `max_buffer_size`, and `number_format`. Parameters not specified in the configuration are either inferred from the data or set to sensible defaults.

### 3.2 Expression matrix reading and validation

The cell expression matrix is read from the HDF5 file. The pipeline validates that the matrix shape matches the number of cells and features as determined by the extracted metadata.

### 3.3 Expression data writing

The expression data, enriched with feature metadata according to the configuration, is written to a Brotli-compressed file (`.br`) in the temporary directory.

### 3.4 Expression metadata reading and writing

Expression metadata from the source attachment is read and transformed according to `columns_to_drop`, `columns_renaming_map`, and `set_column_value`, unless `source_file_metadata` is `false`.

The following statistics are always computed and appended to the metadata regardless of the `source_file_metadata` flag:

1. Total number of cells
2. Total number of features
3. Sparsity (%)
4. Number of non-zero values
5. Source file accession
6. Source file name

The generated metadata file is written to the temporary directory.

---

## Stage 4: Final steps and upload

### 4.1 Dry run halt and validation

If environment variable `dry_run` is `true`, the pipeline performs linking validation and exits at this point. Expression matrix compression is skipped. Logs are reported and available in APIs but not saved as attachments.

When `dry_run` is enabled and the cell linking group has been resolved, the pipeline performs a best-effort linking validation:

- **Biosample coverage:** Unique values in the cell metadata `batch` column are compared against the ID values of the resolved SLP entity. Unmatched values are logged as warnings.
- **Duplicate IDs:** If the same ID value appears in more than one SLP object, a warning is logged (cells could multi-map to multiple entities).
- **Group accession coverage:** Group accessions that contain no biosample objects matching any cell `batch` value are logged as warnings.

Validation mismatches are reported as warnings and do not abort the dry run. Use them to correct the configuration before submitting a full run.

### 4.2 Upload to ODM

Upload proceeds in a fixed order. Deviating from this order would break the linking chain.

**4.2.1 SLP groups**

If `biosample_metadata` is configured with at least one entity:

- **New groups** (for entities with `create_new_group: true`): The corresponding TSV is uploaded as a new group via the entity-specific API endpoint, with `template_id` applied if specified. The new group is then linked to its parent — Sample groups are linked to the study accession; Library and Preparation groups are linked to a Sample group, resolved in this order: (1) `linking_group.sample` in the entity's config, (2) a Sample group created in the same run, (3) pre-fetched Sample group accessions for the study. The new group's accession is stored for use in the cell group linking step (library/preparation takes priority over sample).

- **Existing groups** (for entities with `create_new_group` not set): For each row in the update TSV produced in Stage 2.2, the pipeline calls the ODM PATCH API endpoint for that entity's accession with the new attribute values.

**4.2.2 Cell Group upload**

The transformed cell metadata TSV is uploaded as a new Cell Group, which is linked to the parent SLP Groups determined in Stage 1.3 or resolved in Stage 4.2.1 if new SLP Groups were created.

**4.2.3 Expression Group upload**

The Brotli-compressed expression file and its metadata file are uploaded to create a new Expression Group, which is linked to the newly created Cell Group.

**4.2.4 Log upload**

Transformation logs are uploaded as an attachment together with their metadata. This step is skipped if `save_logs` is `false`.
