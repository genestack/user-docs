---
diataxis: how-to
tab: odm-api
---

# Make your first request in Swagger

This guide walks you through opening the Swagger UI, authorising, and executing your first ODM API request. For how the Swagger UI is organised (its layout, endpoint groups, and definitions), see [Swagger orientation](swagger-orientation.md).

## Open the Swagger UI

From the ODM Dashboard, click **API Documentation**. This opens the Swagger UI in a new window.

## Authorise

Before executing any endpoint, you must authorise:

1. Click **Authorize** (top of the Swagger UI).
2. Select your token type: **Access Token** (Identity Provider Bearer token) or **Genestack API token**.
3. Paste the token value.
4. Click **Authorize**, then **Close**.

Authorisation persists for the duration of your Swagger session. You only need to do this once per session. For how to obtain a token, see [Authentication and tokens](authentication-and-tokens.md).

## Execute a request

1. Expand the endpoint you want to use by clicking on it.
2. Click **Try it out** to enable the input fields. (This step is required for every endpoint you want to execute.)
3. Fill in the required parameters and, if applicable, the request body.
4. Click **Execute**.
5. Review the response body, status code, and headers in the response panel below.
6. Optionally, use the **Download** button to save the response, or copy the generated curl command.
