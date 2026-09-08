---
diataxis: tutorial
tab: odm-api
---

# Tutorial: getting started as an Administrator

In this tutorial, you will use the ODM API to locate detached data objects (objects that have become disconnected from the study hierarchy) and delete an obsolete one. These are the two most common administrative data-management tasks performed via the API.

## Prerequisites

- Both the **Manage organisation** and **Access all data** permissions are required for these operations.
- An API token. See [Authentication and tokens](authentication-and-tokens.md).
- Familiarity with the Swagger UI. See [Swagger orientation](swagger-orientation.md).

## What is a detached object?

A data object is considered detached if it has no direct or indirect link to a root-level study. A study itself is classified as detached if it has no links to lower-level objects.

## Step 1: Find detached objects

1. In the Swagger UI, locate the `manageData` definition.
2. Expand and activate the endpoint **Retrieve a list of detached objects** (`GET /api/v1/manage-data/detached-objects`). Click **Try it out**.
3. Execute the endpoint without any filters to see all available detached objects, or set a page limit (maximum 2000) to reduce the result set.
4. The response lists all detached objects with details including the Genestack accession number, the object type, the owner's email address, and the creation date.
5. Note the `cursor` value at the end of the response. This marks the last retrieved object and lets you continue paginating from where you left off.

## Step 2: Filter by object type

Add a type filter to narrow the results to a specific object class. Accepted type values are: `STUDY`, `SAMPLE_GROUP`, `LIBRARY_GROUP`, `PREPARATION_GROUP`, `TABULAR_DATA`, `GENE_VARIANT`, and `FLOW_CYTOMETRY`.

For example, setting the type filter to `LIBRARY_GROUP` and the limit to `10` returns the first 10 detached library groups.

## Step 3: Delete an obsolete object

> **Warning:** deletion is irreversible. Ensure the accession you supply is correct before proceeding.

1. In the `manageData` definition, expand **Delete a data object or data group** (`DELETE /api/v1/manage-data/data`). Click **Try it out**.
2. Enter the accession number of the object you want to delete (for example, `GSF1147012`).
3. Click **Execute**. An HTTP `202` response confirms that the deletion has been initiated. The operation processes asynchronously.

## Step 4: Verify the deletion

After a short time, search for the deleted study or object in the ODM interface. It should no longer appear in any listing.

## What you built

You have located detached data objects via the API and removed one. For the per-task how-to guides covering these and related admin API operations, see [Administer via API](../admin/index.md).
