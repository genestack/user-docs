# Single-cell data in ODM: Getting started

**Upload → Transform → Index → Search**

This page walks you through the single-cell HDF5 workflow in ODM (uploading a file, running a transformation to produce indexed objects, confirming indexing, and exploring your data with search and analytics queries) and links to the notebooks for each stage.

## Who this is for

This guide is for users who want to try ODM's single-cell functionality on prepared datasets.

## Prerequisites

- ODM instance URL: `<HOST>`
- API token: `<TOKEN>`. See [Authentication and tokens](../../getting-a-genestack-api-token.md).
- An environment set up to run Jupyter notebooks.

---

## Step 1: Upload and transform a single dataset

The goal here is to walk through the full workflow on one HDF5 file and verify that analysis-ready objects appear in ODM.

1. Create a study with an HDF5 file as an attachment.
2. Run a transformation job to convert it into ODM-indexed single-cell objects.
3. Verify that objects were created, linked, and indexed correctly.

**Notebook:** [Single-Cell RNA-Seq: Data Transformation and Upload to ODM](../../doc-odm-user-guide/notebooks/sc_transformations_demo.ipynb)


This notebook covers: uploading the HDF5 file, creating a configuration, running a dry run, and checking job status and outputs.

---

## Step 2: Load curated public datasets

The goal of this optional step is to populate ODM with a ready-made catalogue of curated public single-cell studies so you can test cross-study search without preparing your own data.

1. Load the public dataset template.
   - Template file: [public_studies_template_demo.json](https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/templates/public_studies_template_demo.json)
   - For template upload instructions, see [Create or update a template](../../../../tools/odm-sdk/terminal/templates/create-or-update-template.md).
2. Load the curated datasets (HDF5 attachments included).
   - **Ready-to-run import commands:** [Curated public datasets](curated-public-datasets.md), per-dataset copy-paste commands with placeholders for server, token, and template.

---

## Step 3: Transform curated datasets

The goal is to transform the curated datasets into fully indexed objects with harmonised metadata.

1. Using the transformation notebook from Step 1 as a reference, run the transformation for each curated dataset.
2. Use the provided configurations to ensure consistent curation. You can skip the dry-run step, as the configurations are pre-tested.
3. Monitor transformation jobs until all complete successfully.
4. Confirm that the expected objects are present: Cell Group, Expression Group, and metadata objects.

**Prepared configurations:** [Curated public datasets](curated-public-datasets.md#configuration-index), the configuration to use for each dataset.

---

## Step 4: Confirm indexing

Make sure all datasets are marked as indexed and ready to query.

- Each transformed dataset shows the **Indexed** label in the ODM Metadata Editor.
- All indexing tasks show **Done** status in Task Manager.

> A completed transformation job does not mean data is immediately searchable. ODM automatically triggers indexing after ingestion, but data is only available for querying once indexing finishes.

---

## Step 5: Query and analyse single-cell data

Use ODM's search and analytics notebooks to explore your indexed datasets.

**Notebook:** [Single-Cell RNA-Seq: Cohort Selection and Data Retrieval](../../doc-odm-user-guide/notebooks/sc_rnaseq_demo.ipynb)


This notebook covers: cross-study search examples, filtering by curated attributes, example analytical queries, and result inspection.

---

## Next steps

- [About single-cell transformations](about-single-cell-transformations.md): conceptual overview of the transformation pipeline.
- Per-task how-tos: [Ingest cell and expression data](ingest-cell-and-expression.md), [Create sample/library/preparation groups](create-sample-library-preparation-groups.md), [Update existing biosample metadata](update-existing-biosample-metadata.md), [Discover biosample attributes](discover-biosample-attributes.md).
- [Configuration reference](configuration-reference.md): full configuration schema.
- [Transformation process reference](transformation-process-reference.md): internal processing pipeline.
- [API reference](../api-reference.md): API endpoints.
