# Tutorial: End-to-end Single-Cell Workflow in ODM

**Upload → Transform → Index → Confirm → Query**

---

## Goal

Walk through the complete lifecycle of a single-cell dataset in ODM — from uploading a raw HDF5 file to querying indexed cells and expression data using the provided notebooks.

---

## Prerequisites

- **Role:** Contributor (or Administrator).
- An H5AD file ready to upload (or access to the demo datasets described in Step 2).
- An API token generated in your ODM account.
- ODM instance URL: `<HOST>`

---

## Overview

Single-cell data in ODM is structured around three stages:

1. **Upload** — attach an HDF5 file to a study.
2. **Transform** — run a transformation job to produce indexed Cell Group and Expression Group objects.
3. **Query** — use ODM's search and analytics APIs to explore the indexed data.

This tutorial walks through each stage in order. You will finish with a fully indexed single-cell dataset and working examples of API queries.

---

## Step 1 — Upload and transform a single dataset

**Goal:** Walk through the full workflow on one HDF5 file and verify that analysis-ready objects appear in ODM.

1. Create a study and attach an HDF5 file to it as an attachment.
2. Submit a transformation job to convert the HDF5 file into ODM-indexed single-cell objects.
3. Verify that the expected objects were created, linked, and indexed correctly.

**Notebook:** *Transformation Quickstart*

- Link: [Single-Cell RNA-Seq: Data Transformation and Upload to ODM](../../doc-odm-user-guide/doc-odm-user-guide/notebooks/sc_transformations_demo.ipynb)
- What it covers: uploading the HDF5 file, creating a transformation configuration, running a dry-run to validate the configuration, checking job status and inspecting outputs.

---

## Step 2 — Load curated public datasets

**Goal:** Populate ODM with a ready-made catalogue of curated public single-cell studies so you can test cross-study search without preparing your own data. Loading the provided template enables range queries across harmonised attributes.

1. Load the metadata template:
   - Link: [Public dataset template](https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/templates/public_studies_template_demo.json)
   - Further details: [Template upload guide](../../../docs/tools/odm-sdk/terminal/templates/create-or-update-template.md)
2. Import the curated datasets into ODM (HDF5 attachments included):
   - **Ready-to-run import commands:** [Import commands for public datasets](../../doc-odm-user-guide/doc-odm-user-guide/extras/dataset-import-commands.md) — includes copy-paste commands with placeholders for server, token, and template.
   - Further details: [Uploading studies to ODM](../../../docs/tools/odm-sdk/terminal/study/uploading-study.md)

---

## Step 3 — Transform curated datasets

**Goal:** Transform the curated datasets to produce fully indexed objects with harmonised metadata.

1. Using the Transformation Notebook as a reference, run the transformation for each curated dataset.
2. Use the provided configurations to ensure consistent curation. You can skip the dry-run step for these datasets, as the configurations are pre-tested.
3. Monitor transformation jobs until all complete successfully.
4. Confirm that the expected objects are present for each dataset: Cell Group, Expression Group, and metadata objects.

**Prepared configurations:**

- Link: [Public dataset configurations](../../doc-odm-user-guide/doc-odm-user-guide/extras/public-dataset-configurations-mapping.md)

---

## Step 4 — Confirm indexing completed

**Goal:** Make sure all datasets are marked as indexed and ready to query.

- Each transformed dataset shows the **Indexed** label in the ODM Metadata Editor.
- All indexing tasks show **Done** status in the Task Manager (accessible from the top-right corner of the ODM interface).

> **Note:** A completed transformation job does not mean the data is immediately searchable. ODM automatically triggers indexing after ingestion, but data is available for querying only once indexing finishes. Allow a few minutes after transformation completes before running queries.

---

## Step 5 — Query and analyse single-cell data

**Goal:** Use ODM's search and analytics notebooks to explore your indexed datasets.

**Notebook:** *Single-cell Query and Analysis*

- Link: [Single-Cell RNA-Seq: Cohort Selection and Data Retrieval](../../doc-odm-user-guide/doc-odm-user-guide/notebooks/sc_rnaseq_demo.ipynb)
- What it covers: cross-study search examples, filtering by curated attributes, example analytical queries (differential expression, cell ratio statistics, gene summary), and result inspection.

---

## What happened?

You have completed the full single-cell data lifecycle in ODM:

1. Uploaded an HDF5 file as a study attachment.
2. Created a transformation configuration and submitted a job to produce Cell Group and Expression Group objects.
3. Loaded curated public datasets and transformed them using pre-tested configurations.
4. Confirmed that all datasets are indexed and queryable.
5. Ran cross-study search and analytical queries using the provided notebooks.

---

## What's next?

- [HDF5 transformation how-to guides](../../how-to/single-cell/hdf5-transformations.md) — step-by-step guidance for running and customising transformations.
- [Transformation configuration reference](../../reference/single-cell/transformation-config.md) — full schema for the transformation configuration JSON.
- [Understanding HDF5 transformations](../../explanation/single-cell/hdf5-transformations.md) — conceptual overview of how the transformation pipeline works internally.
