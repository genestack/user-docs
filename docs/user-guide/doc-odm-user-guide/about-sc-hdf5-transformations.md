# Single-Cell HDF5 Transformations Overview

> **Related documentation:** For step-by-step guidance on running the transformation, see the [How-to Guides](how-to-sc-hdf5-transformations.md). For the full configuration schema, see the [Configuration Reference](configuration-reference.md). For the API endpoints, see the [API Reference](api-reference.md). For the internal processing pipeline, see the [Transformation Process Reference](transformation-process-reference.md). For more information related the Single-cell data support in ODM, see the [Working with Single Cell Data](single-cell.md)

This transformation converts a single-cell HDF5 file into the ODM-compatible output files. It extracts expression data and related cell metadata, and can optionally harmonize metadata and create or update biosample objects in ODM. The output files are then imported and linked automatically.

The result is feature-level indexed data that is ready for downstream analysis and cross-study discovery without manual file preparation.

## The ODM entity model for single-cell data

Understanding the transformation requires familiarity with how ODM represents single-cell experiments. ODM organises data around a hierarchy of entities:

- **Sample, Library, and Preparation groups** (collectively referred to as SLP) represent the biological and experimental context of the data. A Sample describes a biological specimen; a Library describes the sequencing library prepared from it; a Preparation describes a preparation step. These entities already exist in ODM for most studies, or can be created by the transformation itself.

- **A Cell Group** represents the collection of individual cells from an experiment, together with their metadata. Each Cell Group must be linked to exactly one parent SLP entity (a Sample, Library, or Preparation group). This linkage is what allows ODM to associate cell-level observations with the correct experimental context.

- **An Expression Group** represents the gene-by-cell expression matrix, compressed for efficient retrieval, together with computed dataset statistics. An Expression Group is always linked to a Cell Group.

The transformation creates the Cell Group and Expression Group and links them into the existing (or newly created) SLP structure. This is why the configuration requires specifying how the resulting Cell Group should be connected to its parent — the linking step is fundamental to how ODM organises and queries the data.

## What the transformation reads from the source file

The transformation extracts three types of data from a HDF5 source file:

**Cell metadata** — extracted primarily from the `obs` in H5AD input file, or the equivalent structure in 10x H5 input. This includes per-cell annotations such as barcodes, cluster assignments, quality control metrics, and any other experimental annotations. Multidimensional representations stored in `obsm` (such as PCA or UMAP coordinates) and pairwise cell annotations from `obsp` can also be extracted.

**Feature metadata** — extracted from `var`, and optionally from `varm` and `varp`. This includes per-gene annotations such as gene identifiers and gene names. For supported species, the transformation can also map Ensembl or NCBI gene identifiers to gene names automatically.

**The expression matrix** — extracted from `X`, which contains count or normalized expression values. The transformation validates the matrix dimensions against the extracted cell and feature metadata, then writes the matrix in a Brotli-compressed format optimized for ODM ingestion.
## The role of metadata curation

Metadata curation is optional, but strongly recommended. It standardizes cell metadata so that it can be imported, linked, and indexed correctly in ODM. Certain fields must use the expected names and data types to ensure consistent linking and indexing. The transformation handles this for the user during processing.

Curation also harmonizes metadata across datasets. This is essential for cross-study search and downstream analysis, because equivalent annotations must be represented consistently. This can include renaming attributes, replacing values with standardized terms, assigning default values, or dropping unnecessary columns. 

Curation is applied only to the data produced by the transformation for import into ODM. The source file is not modified.

## Biosample metadata and the aggregation model

Some single-cell datasets store tissue, disease, or other biosample-level attributes in cell metadata, repeating the same values for every cell. The transformation can aggregate these attributes into related biosample object: Sample, Library, or Preparation (SLP) objects in ODM.

Aggregation is performed by grouping cells using a designated biosample identifier. Only attributes that are consistent across all cells in the same biosample can be assigned to related biosample objects.

Attributes assigned to biosample objects are automatically removed from the cell metadata. This reduces duplication and improves the overall structure of the imported data.

## Linking created objects

When the transformation uploads a Cell Group, it links it to a parent Sample, Library, or Preparation entity (SLP).

This is usually handled automatically. If the transformation creates new SLP objects, the Cell Group is linked to them. Otherwise, the transformation identifies the most appropriate existing SLP target in ODM. Users can override the automatic behavior by specifying the target explicitly in the configuration.
For details, see [Linking group determination](transformation-process-reference.md#13-linking-group-determination).

The created Expression Group created by the transformation is linked to the corresponding Cell Group .

## Dry run mode

Before committing any data to ODM, users can run the transformation in dry run mode. In this mode, the transformation performs all extraction, curation, and validation steps — including resolving the linking target and validating that all cell batch identifiers match existing SLP objects — but uploads nothing. Logs are printed but not saved as attachments.

Dry run mode is particularly useful for exploring which biosample-level attributes are available in a dataset before committing to a curation strategy. When `biosample_metadata` is configured without any `columns_to_export` entries, the dry run will log which columns are uniform per biosample and therefore eligible for export — without creating any files or objects.

The recommended practice is to iterate on the configuration using repeated dry runs until all warnings are resolved before submitting a full transformation run.

## Processors Controller API: configurations, images, and jobs

The transformation is managed through the ODM Processors Controller API. It is based on three related components: configurations, images, and jobs.

**Transformation configurations** are JSON documents that define how input files should be processed, including the input format, metadata extraction, and curation rules. Configurations can be created, retrieved, and updated independently of any particular run. The same configuration can be reused across multiple files with the same structure.

**Transformation images** are versioned container images that run the processing logic. Available image versions can be queried through the API. The image used for single-cell HDF5 files is `hdf5-cells`. When starting a job, users can specify either `latest` or a specific release tag.

**Transformation jobs** are the execution records. A job combines a configuration, an image, and one or more input files, runs the transformation, and produces the output and logs. Jobs are independent, so the same input can be run again with a different configuration or image when needed.

## Transformation logs

Each transformation job produces a log that records the processing steps, warnings, detected issues, and created outputs. The log also includes provenance information, such as the source file name and accession, and the accessions of the created objects.
As part of the transformation, the log is uploaded to ODM and stored with the study as an attachment alongside the other generated files. This provides a persistent record of the transformation output. Logs are also available through the API for a limited time. By default, this retention period is two weeks.

## Supported input formats

The transformation supports the following HDF5-based input formats:

- **H5AD (AnnData)** — the native format of the AnnData Python library, widely used in the single-cell ecosystem.
- **10x Genomics H5** — converted internally to H5AD before processing, so the same extraction workflow is used regardless of the input format.
- **Legacy 10x Genomics H5 (v<3)** — supported only for files containing a single genome. Multi-genome legacy files are not supported.
