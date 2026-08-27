---
diataxis: tutorial
tab: odm-api
---

# Tutorial: getting started as a Data Contributor

In this tutorial, you will create a complete study end-to-end via the ODM API: uploading study metadata, uploading sample metadata, uploading expression data, and then linking all three together. By the end you will have a fully linked study visible in the ODM interface.

## Prerequisites

- Membership in the Curator group.
- An API token. See [Authentication and tokens](authentication-and-tokens.md).
- Familiarity with the Swagger UI. See [Swagger orientation](swagger-orientation.md).
- The following example files (hosted on S3 and available without authentication):
    - [GSE60871_study.tsv](https://bio-test-data.s3.amazonaws.com/GSE60871/GSE60871_study.tsv), study metadata
    - [GSE60871_samples.tsv](https://bio-test-data.s3.amazonaws.com/GSE60871/GSE60871_samples.tsv), sample metadata
    - [GSE60871_expression.gct](https://bio-test-data.s3.amazonaws.com/GSE60871/GSE60871_expression.gct), gene expression in GCT format

## Step 1: Upload study metadata

1. From the ODM Dashboard, click **API Documentation** to open the Swagger UI.
2. Authorise with your token if you have not done so already.
3. Locate the **Job** endpoint group and expand **Import study metadata from a TSV file** (`POST /api/v1/jobs/import/study`). Click **Try it out**.
4. In the parameters section, enter the URL of the study metadata TSV file (e.g., the S3 link above) and click **Execute**.

    > If the request includes a template accession number, replace it with the accession of your desired template, or omit it entirely to use the default template.

## Step 2: Track the import job

1. The response confirms the import has started and includes a `jobExecId` (for example, `1268`). Note this ID.
2. Track the import status using `GET /api/v1/jobs/{jobExecId}/output`. A successful import assigns an accession number to the new study (for example, `GSF1147033`).

**Study Accession ID: `GSF1147033`** (your value will differ)

## Step 3: Upload sample metadata

1. In the Job endpoint group, locate **Import a group of sample metadata objects from a TSV file** (`POST /api/v1/jobs/import/samples`). Click **Try it out**.
2. Enter the URL of the sample metadata TSV file and click **Execute**.

    > Replace the template accession number with the desired template accession.

3. Note the `jobExecId` from the response (for example, `1269`).
4. Check the job status with `GET /api/v1/jobs/{jobExecId}/output`. A successful import returns a Sample Group accession number (for example, `GSF1147034`).

**Sample Group Accession ID: `GSF1147034`** (your value will differ)

## Step 4: Upload expression data

1. In the Job endpoint group, locate **Import any tabular data or GCT files** (`POST /api/v1/jobs/import/expression`). Click **Try it out**.
2. Enter the required parameters: the URL of the expression data file, the template, and the data class. Optionally provide a metadata link.

    > For all `.tsv` files, the `numberOfFeatureAttributes` parameter is mandatory.

3. Note the `jobExecId` from the response (for example, `1271`).
4. Check job status with `GET /api/v1/jobs/{jobExecId}/output`. A successful import returns an accession number for the expression data group (for example, `GSF1147049`).

**Experimental Data Group Accession ID: `GSF1147049`** (your value will differ)

## Step 5: Link samples to the study

Linking must be performed in the correct order: samples to study first, then data to samples.

1. In the definition selector, choose **integrationCurator**. This definition contains the endpoints for linking entities.
2. Expand **Create a Link Between a Group of Sample Objects and a Study** (`POST /api/v1/as-curator/integration/link/sample/group/{sourceId}/to/study/{targetId}`). Click **Try it out**.
3. Enter:
    - `sourceId`: your Sample Group Accession ID (e.g., `GSF1147034`)
    - `targetId`: your Study Accession ID (e.g., `GSF1147033`)
4. Click **Execute**. A response with HTTP status `204` confirms the link was created.

You can open the study in the ODM interface to confirm that the sample metadata is now associated with the study.

## Step 6: Link expression data to the sample group

1. In the **integrationCurator** definition, expand **Create a link between a group of expression objects and a group of samples objects** (`POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/sample/group/{targetId}`). Click **Try it out**.
2. Enter:
    - `sourceId`: your Experimental Data Group Accession ID (e.g., `GSF1147049`)
    - `targetId`: your Sample Group Accession ID (e.g., `GSF1147034`)
    - By default, the linking attribute is **Sample Source ID**. You can customise this to another column if your data uses a different key.
3. Click **Execute**. A response with HTTP status `200` confirms the link was created.

## Step 7: Verify in the ODM interface

Open the ODM interface and navigate to your study. The study now shows the sample metadata and expression data linked. You have successfully created a complete study via the API.

## What you built

You have imported and linked a full study (study metadata, sample metadata, and expression data) using the ODM API. For next steps, explore the per-entity how-to guides in [Contribute via API](../contribute/index.md) and reference the import job endpoints in depth.
