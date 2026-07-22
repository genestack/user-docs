---
diataxis: how-to
tab: odm-api
---

# How to run cross-product queries

This guide shows you how to query across linked entity types in ODM (for example, retrieving the samples linked to a library, or the preparations linked to a sample) using the integration endpoints.

For filter syntax and URL-encoding rules, see [Query and filter syntax reference](../reference/query-and-filter-syntax-reference.md). For the complete parameters and response schema of any endpoint, see the [Swagger UI](/swagger/helper/).

## Prerequisites

- An API token. See [Authentication and tokens](../getting-started/authentication-and-tokens.md).
- The entities you want to query must already be linked. Linking is performed at import time. See [Link entities after import](../contribute/import-data/link-entities-after-import.md).

## About cross-product queries

ODM's integration endpoints let you traverse the entity graph: you filter one entity type based on metadata conditions on another linked entity type. For an overview of the integration endpoint model, see [About querying data](about-querying-data.md).

The endpoints follow a consistent pattern, so once you know the shape you can construct any traversal:

```
GET /api/v1/as-curator/integration/link/{target-type}/by/{source-type}
```

For example, `.../link/samples/by/libraries` retrieves samples linked to libraries, and `.../link/preparations/by/samples` retrieves preparations linked to samples. User-access equivalents (`as-user/`) are available for all of these.

## Retrieve samples linked to a library

Pass a URL-encoded `filter` to restrict the source entities. This retrieves sample metadata for samples linked to libraries with Library ID `LIB1`:

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/as-curator/integration/link/samples/by/libraries?filter=%22Library%20ID%22%3D%20LIB1' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

## Retrieve preparations linked to a sample

This retrieves preparation metadata for preparations linked to samples with Sample Source ID `HG00119`:

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/as-curator/integration/link/preparations/by/samples?filter=%22Sample%20Source%20ID%22%20%3D%20HG00119' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

## Reading the response

Integration responses pair a `meta.pagination` block with a `data` array. Each item carries the entity's accession, its metadata attributes, and a `groupId` identifying the parent group object:

```json
{
  "meta": { "pagination": { "count": 2, "total": 2, "offset": 0, "limit": 2000 } },
  "data": [
    {
      "genestack:accession": "GSF1283543",
      "Sample Source ID": "SRR6441188",
      "groupId": "GSF1283541"
    }
  ]
}
```
