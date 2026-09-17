---
diataxis: how-to
tab: odm-api
---

# How to search attached files via the API

This guide shows you how to find attached files and download them through the ODM REST API.

For filter syntax, see [Query and filter syntax reference](../reference/query-and-filter-syntax-reference.md). For the complete parameters and response schema of any endpoint, see the [Swagger UI](/swagger/helper/).

## Prerequisites

- An API token. See [Authentication and tokens](../getting-started/authentication-and-tokens.md).
- The study containing the files must be shared with you, or you must have the "Access all data" permission.

Attached files are not content-indexed; they can only be queried by their metadata. For background on the distinction between indexed and attached files, see [About querying data](about-querying-data.md).

> **Note:** attaching a valid expression matrix to a study does not index it. Attached expression files are not accessible via the omics query endpoints.

## Find attached files by metadata

Send `GET /api/v1/as-user/files` (or `as-curator`) to retrieve the attached files accessible to you, narrowing the result with metadata filters such as `query` and `dataClass`. To retrieve a single file directly, send `GET /api/v1/as-user/files/{id}` with its Genestack accession.

## Find the files attached to a study

Send `GET /api/v1/as-user/integration/link/files/by/study/{id}` to retrieve every file attached to a specific study:

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/as-user/integration/link/files/by/study/GSF1280195?includeContents=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

If the study has no attached files, the response is an empty array `[]`.

## Find studies by their attached files

To go the other way (from files to the studies that contain them), send `GET /api/v1/as-user/integration/link/studies/by/files` (or `as-curator`), filtering by file metadata.

For files with internal structure such as HDF5, add `includeContents=true` to include the parsed structure in the response. To search *by* that structure, see [Search by HDF5 contents](search-by-hdf5-contents.md).

## Download an attached file

Send `GET /api/v1/as-user/files/{id}/download` (or `as-curator`) to download a file by its accession; it is fetched from storage and returned as a downloadable response, subject to your access permissions. For batch-download workflows, send `HEAD /api/v1/as-user/files/{id}/download` first to retrieve metadata-only headers before downloading.
