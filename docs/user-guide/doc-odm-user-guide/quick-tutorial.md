# Single-cell data in ODM: End-to-end guide
**Upload → Transform → Index → Search**

---

### Who this is for
Users who want to bring single-cell data (HDF5 / H5AD / 10x H5) into ODM, index it, and run cross-study queries.

### What you'll achieve
- Upload single-cell input files as attachments.
- Run the transformation to generate ODM-compatible indexed objects.
- Query the data using the provided notebooks.

### Prerequisites
- ODM instance URL: `<HOST>`
- API token: `<TOKEN>`
- Environment to run the notebooks.

---

## Step 1 — Upload and transform a single dataset

**Goal:** Try the full workflow on one HDF5 file and see analysis-ready objects in ODM.

1. Create a study with an HDF5 file as an attachment.
2. Run a transformation job to convert it into ODM-indexed single-cell objects.
3. Verify objects were created, linked, and indexed correctly.

**Notebook:** *Transformation Quickstart*
- Link: [Single-cell RNA-Seq: Data transformation and upload to ODM](doc-odm-user-guide/notebooks/transformations-demo.ipynb)
- What it covers: uploading the HDF5 file · creating a configuration · running a dry-run · checking job status and outputs.

---

## Step 2 — Load curated public datasets

**Goal:** Get a ready catalogue of curated public single-cell studies to test cross-study search without preparing your own data. Load data using the template created for these datasets to enable range queries.

1. Load the template — `<TEMPLATE_LINK_PLACEHOLDER>` · [Template upload guide](../../../docs/tools/odm-sdk/terminal/templates/create-or-update-template.md)
2. Load the curated datasets into ODM (HDF5 attachments included).

**Ready-to-run import commands:**
- Link: [Import commands for public datasets](doc-odm-user-guide/extras/dataset-import-commands.md)
- Includes copy/paste commands with placeholders for server and token.
- Further details: [Uploading studies to ODM](../../../docs/tools/odm-sdk/terminal/study/uploading-study.md)

---

## Step 3 — Transform curated datasets

**Goal:** Transform the curated datasets to create fully indexed objects with harmonised metadata.

1. Using the Transformation Notebook as an example, run the transformation for each curated dataset.
2. Use the provided configurations to ensure consistent curation. Dry-run can be skipped as configurations are pre-tested.
3. Monitor jobs until all succeed.
4. Confirm expected objects exist: Cell Group, Expression Group, metadata objects.

**Prepared configurations:**
- Link: [Public dataset configurations](doc-odm-user-guide/extras/)
- Configuration-to-dataset mapping table: [Configuration mapping](doc-odm-user-guide/extras/public-dataset-configurations-mapping.md)

---

## Step 4 — Confirm indexing completed

**Goal:** Ensure datasets are marked as indexed and ready to query.

- Each transformed dataset shows the **Indexed** label in ODM Metadata Editor.
- All indexing jobs show **Done** status in Task Manager.

---

## Step 5 — Query and analyse single-cell data

**Goal:** Use ODM search and analytics notebooks to explore indexed datasets.

**Notebook:** *Single-cell Query & Analysis*
- Link: - [Single-cell RNA-Seq: Cohort Selection and Data Retrieval](doc-odm-user-guide/notebooks/sc_rnaseq_demo.ipynb)
- What it covers: cross-study search examples · filtering by curated attributes · example analytical queries and result inspection.
