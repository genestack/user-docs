# Tutorial: Single-Cell HDF5 Transformation and Upload to ODM

This tutorial walks you through an interactive Jupyter notebook that demonstrates the full workflow for transforming and uploading a single-cell RNA-seq HDF5 file to ODM using the Processors Controller API.

---

## Goal

By the end of this tutorial you will know how to:

- Import a raw H5AD file and its associated metadata into ODM.
- Create and manage a transformation configuration.
- Run a transformation job in `dry_run` mode to validate the configuration without modifying data.
- Iterate on the configuration based on dry-run log output.
- Submit the final transformation job and verify the resulting Cell Group, Expression Group, and biosample metadata updates.
- Query the indexed expression data via the ODM Omics API.

---

## Prerequisites

- Completed the [End-to-end single-cell workflow](sc-workflow.md) tutorial, or have an existing ODM study to work with.
- Python 3.10 or later with `pip`.
- Required Python packages (install with pip):
  ```
  pip install pandas ipython ipywidgets python-dotenv odm-sdk anndata scipy scanpy matplotlib
  ```
- An API token for your ODM instance (generate it from your ODM account settings).
- An H5AD file ready to upload. The notebook uses a publicly available fibrotic liver scRNA-seq dataset (Watson et al., 2023, GEO: GSE210077) as the demo input.

---

## Download the Notebook

[sc_transformations_demo.ipynb](../../doc-odm-user-guide/doc-odm-user-guide/notebooks/sc_transformations_demo.ipynb)

Open the downloaded file in JupyterLab or Jupyter Notebook.

---

## What You'll Learn

The notebook is organised into four main sections:

### Section 1 — Prerequisites

Sets up the Python environment. This section:

- Installs and imports all required libraries (`odm_api`, `anndata`, `scanpy`, `matplotlib`, and others).
- Defines utility functions used throughout the notebook, including API credential helpers, log parsing, and display helpers for transformation job output.

### Section 2 — ODM API Configuration

Establishes a connection to your ODM instance. This section:

- Prompts you to enter your ODM instance URL and API token. The token can be read from a `.env` file (`ODM_API_TOKEN`) or entered interactively via `getpass`.
- Initialises the `odm_api.ApiClient` that all subsequent API calls use.

### Section 3 — Data Import

Imports the demo dataset into ODM using the `odm-import-data` CLI tool. This section:

- Uploads study metadata, sample metadata, library metadata, and the H5AD file as an attachment to a new study in ODM.
- Extracts the attachment accession from the import logs — this accession is required when submitting the transformation job.

You can substitute the demo dataset URLs with your own study, sample, and file paths.

### Section 4 — Working with Processors Controller API Endpoints

The core of the tutorial, organised into three subsections:

**4.1 Transformation Configuration**

A transformation configuration is a JSON document stored in ODM that describes how the source HDF5 file should be processed — which layers to extract, how to rename and curate columns, and what data class to assign to the Expression Group.

This subsection shows how to:

- List existing configurations already stored in your ODM instance.
- Create a minimal baseline configuration (`file_type`, `cell_metadata`, `feature_metadata`, `cell_expression`) using `post_api_v1_transformations_configurations()`.
- Retrieve the assigned configuration ID, which is needed for job submission.
- Update the configuration in-place with `put_api_v1_transformations_configurations_by_id()` after the dry-run reveals issues.

The section also walks through a realistic example of what a modified configuration looks like: renaming columns, exporting biosample attributes, curating linking-column values, and including `obsm`/`obsp` embeddings.

**4.2 Transformation Images**

A transformation image is the versioned container that executes the processing logic. This subsection shows how to:

- List all available transformation images using `list_api_v1_transformations_images()`.
- Identify the `hdf5-cells` image, which handles H5AD and H5 input formats and produces Cell Group, Expression Group, and biosample outputs.
- Understand the `latest` version tag and when to pin to a specific version for reproducibility.

**4.3 Transformation Jobs**

This is the workflow execution section. It covers three stages:

1. **Dry-run job (4.3.1):** Submit the job with `dry_run=True`. The pipeline runs all metadata extraction and curation steps without uploading anything to ODM. Review the structured logs to identify column naming issues, missing required fields (`barcode`, `batch`), or unexpected file structure. Update the configuration and re-run until the dry run completes with status `DONE`.

2. **Full transformation job (4.3.2):** Submit the same job with `dry_run=False`. The pipeline:
   - Validates the configuration and retrieves attachment metadata.
   - Extracts and curates cell metadata, feature metadata, and biosample attributes.
   - Compresses the expression matrix using Brotli.
   - Uploads Cell Group, Expression Group, and SLP updates to ODM.
   - Links all objects into the study hierarchy and saves the transformation log as an attachment.

3. **Inspecting results (4.3.3):** After the full job completes, use the group accessions extracted from the job logs to verify:
   - Updated biosample attributes (exported columns are merged into the Sample group).
   - Cell metadata stored in the Cell Group.
   - Expression Group summary statistics (cell count, feature count, sparsity).
   - Expression data queried via `OmicsQueriesAsUserApi` with cell-level quality filters, assembled into an `AnnData` object, and visualised as violin plots.

---

## What's next?

- [Transformation configuration reference](../../reference/single-cell/transformation-config.md) — complete schema documentation for all configuration fields, including all supported `metadata_keys`, `columns_renaming_map`, `columns_to_curate_values`, and biosample export options.
- [Example transformation configurations](../../reference/single-cell/example-configs.md) — annotated real-world configurations for common HDF5 layouts.
