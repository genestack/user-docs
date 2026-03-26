# About Single-Cell HDF5 Transformations in ODM

> **Related documentation:** For step-by-step guidance on running the transformation, see the [How-to Guides](how-to-sc-hdf5-transformations.md). For the full configuration schema, see the [Configuration Reference](configuration-reference.md). For the API endpoints, see the [API Reference](api-reference.md). For the internal processing pipeline, see the [Transformation Process Reference](transformation-process-reference.md).

Single-cell datasets are commonly distributed as HDF5-based files — most often H5AD (the AnnData format) or the 10x Genomics H5 format. While these formats are rich and expressive, they are not directly ingestible into ODM in a way that supports consistent indexing, cross-dataset search, and the entity relationships that ODM relies on for downstream discovery.

The single-cell HDF5 transformation exists to bridge this gap. Rather than requiring users to hand-craft intermediate files or manually restructure their data, the transformation automates the entire end-to-end process: reading the source file, extracting and optionally curating the relevant metadata, and uploading the results as structured ODM objects.

## The ODM entity model for single-cell data

Understanding the transformation requires familiarity with how ODM represents single-cell experiments. ODM organises data around a hierarchy of entities:

- **Sample, Library, and Preparation groups** (collectively referred to as SLP) represent the biological and experimental context of the data. A Sample describes a biological specimen; a Library describes the sequencing library prepared from it; a Preparation describes a preparation step. These entities already exist in ODM for most studies, or can be created by the transformation itself.

- **A Cell Group** represents the collection of individual cells from an experiment, together with their metadata. Each Cell Group must be linked to exactly one parent SLP entity (a Sample, Library, or Preparation group). This linkage is what allows ODM to associate cell-level observations with the correct experimental context.

- **An Expression Group** represents the gene-by-cell expression matrix, compressed for efficient retrieval, together with computed dataset statistics. An Expression Group is always linked to a Cell Group.

The transformation creates the Cell Group and Expression Group and links them into the existing (or newly created) SLP structure. This is why the configuration requires specifying how the resulting Cell Group should be connected to its parent — the linking step is fundamental to how ODM organises and queries the data.

## What the transformation reads from the source file

The transformation extracts three distinct types of data from a single HDF5 source file:

**Cell metadata** comes primarily from the `obs` slot of an H5AD file (or its equivalent in a 10x H5 file). This includes per-cell annotations such as barcodes, cluster assignments, quality control metrics, and any experimental annotations attached to individual cells. Multidimensional representations (such as PCA or UMAP coordinates stored in `obsm`) and pairwise cell annotations (from `obsp`) can also be extracted.

**Feature metadata** comes from `var` (and optionally `varm` and `varp`). This includes per-gene annotations such as gene identifiers and names. The transformation can automatically map Ensembl or NCBI gene IDs to gene names for supported species, avoiding the need to pre-process gene annotation separately.

**The expression matrix** is the count or normalized values matrix (`X`). The transformation validates its dimensions against the extracted cell and feature metadata, then writes it in a Brotli-compressed format optimised for ODM ingestion.

## The role of metadata curation

Raw single-cell datasets frequently contain metadata that needs adjustment before it is useful in a cross-study context. Column names may differ between studies, values may be inconsistently coded, fields may be missing, or the biosample identifiers in the cell metadata may not match the naming conventions used by ODM's SLP entities.

The transformation addresses this through a set of configurable column operations applied during extraction. These include renaming columns, dropping irrelevant fields, filling missing values with defaults, and replacing specific values with standardized equivalents. Attribute names are also mapped to ODM standard names where applicable; non-standard names are automatically converted to camelCase to satisfy the ODM API requirements.

This curation happens in-pipeline, which means the source file is never modified. The curated output exists only as intermediate files in a temporary directory and, ultimately, as the uploaded ODM objects.

## Biosample metadata and the aggregation model

A particularly important feature of the transformation is its ability to derive Sample, Library, or Preparation-level metadata directly from the cell metadata. In many single-cell datasets, attributes such as tissue type, disease condition, or donor information are stored as cell-level annotations (one value per cell), even though they logically belong at the biosample level.

The transformation can aggregate these cell-level attributes to the biosample level by grouping cells by a designated biosample identifier column. Only attributes that are constant across all cells belonging to the same biosample are considered eligible for export to SLP metadata. This ensures that the resulting biosample records are coherent and that no per-cell variation is incorrectly collapsed into a biosample-level value.

Attributes exported to biosample metadata are automatically removed from the cell metadata, preventing duplication. If a biosample attribute should remain in the cell metadata for other reasons, it must be explicitly retained by omitting it from `cell_metadata.columns_to_drop`.

## The linking resolution rules

When the transformation uploads a Cell Group, it must link it to a parent SLP entity. The transformation resolves this target using a defined priority order, so that users do not always need to specify the target explicitly:

1. If the configuration creates new SLP groups, the Cell Group is linked to those newly created groups after they are uploaded.
2. If `cell_metadata.linking_group` explicitly names a target (a sample, library, or preparation accession), that target is used directly.
3. If no explicit target is given, the transformation auto-discovers the appropriate SLP groups for the study from ODM, checking first for Library groups, then Preparation groups, then Sample groups. The first entity type that has at least one group associated with the study is used, and all accessions of that type are linked.

This priority order reflects the typical ODM study structure: Library groups are usually the most specific and appropriate parent for a Cell Group. If a study only has Sample-level grouping, the transformation falls back gracefully.

## Dry run mode

Before committing any data to ODM, users can run the transformation in dry run mode. In this mode, the transformation performs all extraction, curation, and validation steps — including resolving the linking target and validating that all cell batch identifiers match existing SLP objects — but uploads nothing. Logs are printed but not saved as attachments.

Dry run mode is particularly useful for exploring which biosample-level attributes are available in a dataset before committing to a curation strategy. When `biosample_metadata` is configured without any `columns_to_export` entries, the dry run will log which columns are uniform per biosample and therefore eligible for export — without creating any files or objects.

The recommended practice is to iterate on the configuration using repeated dry runs until all warnings are resolved before submitting a full transformation run.

## The API layer: configurations, images, and jobs

The transformation is triggered and managed through the ODM Processors Controller API. This API models the workflow as three separate concerns, each of which can be managed independently:

**Transformation configurations** are stored JSON documents that describe how a source file should be processed: the input file format, which metadata to extract, and any curation rules to apply. Configurations are created, retrieved, and updated independently of any particular run. This separation means you can refine a configuration through many dry-run iterations without losing the history of changes, and reuse the same configuration across multiple runs or files.

**Transformation images** are versioned, containerized environments that execute the processing logic for a given file format. The image used for single-cell HDF5 files is called `hdf5-cells`. Specifying an image version (e.g. `"latest"` or a specific release tag) allows reproducibility and controlled upgrades when new versions are released.

**Transformation jobs** are the actual execution records. A job binds a configuration and an image to one or more input file accessions, runs the processing pipeline, and produces a log. Each job is independent: you can re-run with a different configuration or image without affecting previous jobs or their results.

This design allows the configuration to evolve (through iterations of the iterative dry-run cycle) while keeping the job history clean and auditable.

## Supported input formats

The transformation supports the following HDF5-based input formats:

- **H5AD (AnnData)** — the native format of the AnnData Python library, widely used in the single-cell ecosystem.
- **10x Genomics H5** — converted internally to H5AD before processing, so the extraction logic is unified regardless of the source format.
- **Legacy 10x Genomics H5 (v<3)** — supported provided the file contains a single genome. Multi-genome legacy files are not supported.
