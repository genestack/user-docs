---
diataxis: tutorial
tab: odm-api
---

# Tutorial: getting started as a Data Consumer

In this tutorial, you will retrieve study metadata for a specific study using the ODM API. By the end you will have made a successful API call and inspected the response.

## Prerequisites

- Familiarity with the Swagger UI. See [Swagger orientation](swagger-orientation.md).
- A study to retrieve. In this tutorial we use the accession `GSF1102568` (the study "Study for Demo 2024").

## Step 1: Open API Documentation and select the studyUser definition

From the ODM Dashboard, click **API Documentation**. In the definition selector that appears, find and click **studyUser** to open the Swagger UI. This definition contains the endpoints for retrieving study metadata in read-only mode.

You do not need a token in Swagger. See [Make your first request in Swagger](make-your-first-request.md).

## Step 2: Select the endpoint

Make sure **studyUser** is selected in the top-right definition selector, then locate and expand the endpoint **List or search for study metadata objects** (`GET /api/v1/as-user/studies`). Click on it to see its parameters, response schema, and available filters.

## Step 3: Add the accession to the query parameter

Click **Try it out** to enable the input fields. In the `query` field, enter the study accession number: `GSF1102568`. (To find a study's accession number in the ODM UI, click the top bar of the study and select **Copy accession**.)

## Step 4: Execute and inspect the response

Click **Execute**. The response panel below the endpoint shows the JSON response body containing the study metadata, the HTTP status code, and the response headers. You can optionally download the JSON file using the **Download** button.

## What you built

You have retrieved study metadata for a specific study via the ODM API. From here, you can explore the other endpoints in the `studyUser` definition to retrieve individual studies by accession, or move to the deeper how-to guides in [Explore via API](../explore/index.md) to query samples, expression data, and more.
