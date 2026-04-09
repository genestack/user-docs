# Single-cell data in ODM: Getting Started
**Upload → Transform → Index → Search**

---

## Overview

### Who this is for
Users who want to try single-cell data functionality in ODM on prepared, curated datasets.

### What you'll achieve
- Upload single-cell input files as attachments.
- Run the transformation to generate ODM-compatible indexed objects.
- Try cross-study search and analytical queries using the provided notebooks.

### Prerequisites
- ODM instance URL: `<HOST>`
- API token: `<TOKEN>`
- An environment set up to run the notebooks.

---

## Step 1 — Upload and transform a single dataset

**Goal:** Walk through the full workflow on one HDF5 file and verify that analysis-ready objects appear in ODM.

1. Create a study with an HDF5 file as an attachment.
2. Run a transformation job to convert it into ODM-indexed single-cell objects.
3. Verify that objects were created, linked, and indexed correctly.

**Notebook:** *Transformation Quickstart*
- Link: [Single-Cell RNA-Seq: Data Transformation and Upload to ODM](doc-odm-user-guide/notebooks/sc_transformations_demo.ipynb)
- What it covers: uploading the HDF5 file · creating a configuration · running a dry-run · checking job status and outputs.

---

## Step 2 — Load curated public datasets

**Goal:** Populate ODM with a ready-made catalogue of curated public single-cell studies so you can test cross-study search without preparing your own data. Load the data using the template provided for these datasets to enable range queries.

1. Load the template
  - Link: [Public dataset template](https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/templates/public_studies_template_demo.json)
  - Further details: [Template upload guide](../../../docs/tools/odm-sdk/terminal/templates/create-or-update-template.md)
2. Load the curated datasets into ODM (HDF5 attachments included).
  - **Ready-to-run import commands:** [Import commands for public datasets](doc-odm-user-guide/extras/dataset-import-commands.md). Includes copy-paste commands with placeholders for server, token and template.
  - Further details: [Uploading studies to ODM](../../../docs/tools/odm-sdk/terminal/study/uploading-study.md)

---

## Step 3 — Transform curated datasets

**Goal:** Transform the curated datasets to produce fully indexed objects with harmonised metadata.

1. Following the Transformation Notebook as a reference, run the transformation for each curated dataset.
2. Use the provided configurations to ensure consistent curation. You can skip the dry-run step, as the configurations are pre-tested.
3. Monitor transformation jobs until all complete successfully.
4. Confirm that the expected objects are present: Cell Group, Expression Group, and metadata objects.

**Prepared configurations:**
- Link: [Public dataset configurations](doc-odm-user-guide/extras/public-dataset-configurations-mapping.md)

---

## Step 4 — Confirm indexing completed

**Goal:** Make sure all datasets are marked as indexed and ready to query.
- Each transformed dataset shows the **Indexed** label in ODM Metadata Editor.
- All indexing tasks show **Done** status in Task Manager.

> **Note:** A completed transformation job does not mean the data is immediately searchable. ODM automatically triggers indexing after ingestion, but data is available for querying once indexing finishes.

---

## Step 5 — Query and analyse single-cell data

**Goal:** Use ODM's search and analytics notebooks to explore your indexed datasets.

**Notebook:** *Single-cell Query & Analysis*
- Link: [Single-Cell RNA-Seq: Cohort Selection and Data Retrieval](doc-odm-user-guide/notebooks/sc_rnaseq_demo.ipynb)
- What it covers: cross-study search examples · filtering by curated attributes · example analytical queries and result inspection.


## Next steps

- [Single-Cell HDF5 Transformations Overview](about-sc-hdf5-transformations.md) — conceptual overview of the transformation pipeline.
- [How-to Guides](how-to-sc-hdf5-transformations.md) — step-by-step guidance for running the transformation.
- [Configuration Reference](configuration-reference.md) — full configuration schema.
- [Transformation Process Reference](transformation-process-reference.md) — internal processing pipeline.
- [API Reference](api-reference.md) — API endpoints.
