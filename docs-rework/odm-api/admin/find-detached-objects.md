---
diataxis: how-to
tab: odm-api
---

# How to find detached objects

Failed or half-finished imports can leave objects stranded in ODM: a study with nothing linked to it, or samples that never made it onto a study. Nothing points to them, and nothing surfaces them in normal browsing, so before you can clean them up you have to go looking. This guide shows you how to list detached objects, narrow them down by type, and read what comes back so you know exactly what you are dealing with.

For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## What counts as detached

A data object is detached when it has no direct or indirect link to a root-level object (a study). A study itself counts as detached when it has no links to any lower-level objects.

## Prerequisites

- An API token. See [Authentication and tokens](../getting-started/authentication-and-tokens.md).
- "Manage organisation" AND "Access all data" permissions.

## List the detached objects

Called without any filters, this endpoint returns every detached object available to you, up to 2,000 results:

```text
GET /api/v1/manage-data/detached-objects
```

## Narrow the results by type

To focus on one kind of object, add a `type` filter. The supported values are:

- `STUDY`
- `SAMPLE_GROUP`
- `LIBRARY_GROUP`
- `PREPARATION_GROUP`
- `TABULAR_DATA`
- `GENE_VARIANT`
- `FLOW_CYTOMETRY`

For example, filtering by `LIBRARY_GROUP` returns only detached library group objects.

## Read the response

Each object in the response tells you what it is and who owns it:

- Genestack accession
- Type of the detached object
- Owner email address
- Date of creation

The response also carries a `cursor` field marking the last object retrieved. Pass that value to your next request to page through the full list.

## Next steps

The accessions you collect here are what you feed into deletion. When you are ready to remove the objects you found, see [Delete data](delete-data.md).
