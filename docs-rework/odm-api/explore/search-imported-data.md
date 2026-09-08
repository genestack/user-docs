---
diataxis: how-to
tab: odm-api
---

# How to search imported data via the API

This guide shows you how to query indexed expression, variant, and flow cytometry data through the ODM REST API.

For the filter parameters and their syntax, see [Query and filter syntax reference](../reference/query-and-filter-syntax-reference.md). For the complete parameters and response schema of any endpoint, see the [Swagger UI](/swagger/helper/).

## Prerequisites

- An API token. See [Authentication and tokens](../getting-started/authentication-and-tokens.md).
- The data you want to query must have been indexed on import. Attached files (PDFs, archives) cannot be queried via these endpoints. See [About querying data](about-querying-data.md) for background on the indexed vs. attached distinction.

## Query a data type

Each indexed data type has its own endpoint pair, a user path and a curator path, the latter additionally returning unpublished data:

- **Expression data:** `GET /api/v1/as-user/omics/expression/data` (or `as-curator`)
- **Variant data:** `GET /api/v1/as-user/omics/variant/data` (or `as-curator`)
- **Flow cytometry data:** `GET /api/v1/as-user/omics/flow-cytometry/data` (or `as-curator`)

Called without filters, an endpoint returns all data of that type available to you. Use the filter parameters below to narrow the result.

## Filter to the data you need

Each data type accepts a metadata filter and a value query: `exFilter`/`exQuery` for expression, `vxFilter`/`vxQuery` for variants, and the equivalent pair for flow cytometry. For example, `exQuery=feature.Genes="ZNF814"` returns only expression records for that gene. See [Query and filter syntax reference](../reference/query-and-filter-syntax-reference.md#query-parameters-by-data-type) for the full parameter list and syntax.

## Find variants by gene or VCF INFO field

For variant data, three parameters introduced in release 1.59 target common goals directly:

- **`variantFeature`** finds all variants in a named gene by resolving it to genomic intervals via the reference genome.
- **`variantInfo`** filters on VCF INFO field values (exact match, exclusion, and existence checks).
- **`referenceGenomeId`** restricts variant groups to a specific reference genome.

See the [variant parameters](../reference/query-and-filter-syntax-reference.md#variant-data) in the syntax reference for the exact expressions each one accepts.

## Response format

Search endpoints return a cursor-paginated `data` array in the `multi_values` format (the default since release 1.58). For the full field-by-field structure, see [Response format changes reference](../reference/response-format-changes-reference.md).

To page through results, use the `cursor` value from the previous response to retrieve the next page.

## Example: find expression data linked to a study

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/as-user/integration/link/expression/group/by/study/GSF986326' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

This returns all indexed expression data groups linked to the study `GSF986326`.
