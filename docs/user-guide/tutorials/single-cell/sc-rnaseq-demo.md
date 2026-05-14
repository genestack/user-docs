# Tutorial: Single-Cell RNA-Seq Cohort Selection and Data Retrieval

This tutorial walks you through an interactive Jupyter notebook that demonstrates how to use the ODM API to select a cohort of single-cell RNA-seq samples, retrieve cell and expression data, and perform analytical queries — all programmatically.

---

## Goal

By the end of this tutorial you will know how to:

- Connect to an ODM instance using an API token.
- Search for samples and cells using metadata filters.
- Retrieve expression data for specific genes across a cohort.
- Run analytical queries: cell ratio statistics, differential expression, and gene summary statistics.
- Visualise results using UMAP, violin plots, and volcano plots.

---

## Prerequisites

- Python 3.10 or later with `pip`.
- Required Python packages (install with pip):
  ```
  pip install numpy pandas matplotlib seaborn scipy ipywidgets ipykernel requests scanpy anndata itables plotly nbformat python-dotenv odm-sdk
  ```
- An API token for your ODM instance (generate it from your ODM account settings).
- A public ODM instance or a local install with single-cell data already indexed (see [End-to-end single-cell workflow](sc-workflow.md) to set one up).

---

## Download the Notebook

[sc_rnaseq_demo.ipynb](../../doc-odm-user-guide/doc-odm-user-guide/notebooks/sc_rnaseq_demo.ipynb)

Open the downloaded file in JupyterLab or Jupyter Notebook.

---

## What You'll Learn

The notebook is organised into three main parts:

### Part 1 — Prerequisites (Section 1)

Sets up the Python environment. This section:

- Installs and imports all required libraries (`scanpy`, `anndata`, `plotly`, `odm_api`, and others).
- Defines utility functions used throughout the notebook, including API credential helpers, matrix construction, and visualisation helpers. You can collapse this section once your environment is ready.

### Part 2 — ODM API Configuration (Section 2)

Establishes a connection to your ODM instance. This section:

- Prompts you to enter your ODM instance URL and API token. The token can be read from a `.env` file (`ODM_API_TOKEN`) or entered interactively via `getpass`.
- Initialises the `odm_api.ApiClient` that all subsequent API calls use.

### Part 3 — Working with Data (Sections 3.1 – 3.8)

The main analytical content. Each subsection is independent — you can run them in sequence or jump to the one most relevant to your analysis:

**3.1 Exploring Omics Query Endpoints**
Lists all available omics query methods on the `OmicsQueriesAsUserApi` client. This gives you an overview of the data types (cells, expression, variants, flow cytometry) accessible through the API.

**3.2 Samples**
Searches for samples matching a metadata filter — in the demo, left ventricle samples from patients with hypertrophic cardiomyopathy aged 30–50. Shows how to convert the API response into a pandas DataFrame and summarise attribute distributions.

**3.3 Cells**
Retrieves high-quality cells from the selected samples by applying cell-level quality control filters (mitochondrial percentage and UMI count thresholds). Builds a combined cell metadata table and visualises cell type populations on a UMAP using `scanpy`.

**3.4 Cell Expression Data**
Queries per-cell expression values for a panel of cell-type marker genes. Assembles the expression data into an `AnnData` object and visualises gene expression on the UMAP and as violin plots grouped by cell type.

**3.5 Retrieving Analytical Omics Endpoints**
Lists the analytical endpoints available on `BETAAnalyticsOmicsQueriesAsUserApi`: cell ratio, differential expression, and gene summary.

**3.6 Cell Ratio Statistics**
Computes the proportion of cells belonging to specific subtypes (e.g. `Activated_fibroblast` vs. `Fibroblast_I`) relative to the full quality-filtered cohort. Useful for assessing subpopulation composition across samples.

**3.7 Differential Expression Analysis**
Runs a differential expression comparison between two cell populations across all genes in the cohort. Retrieves results in paginated chunks, calculates log2 fold change and -log10 p-value, and renders an interactive volcano plot with `plotly`.

**3.8 Gene Summary Statistics**
Retrieves per-gene expression distribution statistics (mean, median, standard deviation, quantiles) for selected genes within defined cell populations. Visualises the distributions as boxplots for the top differentially expressed genes, and also demonstrates cross-database gene expression lookup.

---

## What's next?

- [Transformations demo notebook](sc-transformations-demo.md) — learn how to upload and transform your own HDF5 file before querying it.
- [Transformation configuration reference](../../reference/single-cell/transformation-config.md) — understand the configuration options that control how your HDF5 file is processed during transformation.
