---
diataxis: how-to
tab: odm-api
---

# How to search studies via the API

This guide shows you how to find studies and samples through the ODM REST API, from matching on metadata to running a full-text search across everything linked to a study.

For the filter and query syntax used throughout, see [Query and filter syntax reference](../reference/query-and-filter-syntax-reference.md). For the complete parameters and response schema of any endpoint, see the [Swagger UI](/swagger/helper/).

## Prerequisites

- An API token. See [Authentication and tokens](../getting-started/authentication-and-tokens.md).

## Find studies matching metadata criteria

Send `GET /api/v1/as-user/studies` with a `filter` (metadata attribute values) or `query` (keyword search) parameter to find studies. For example, `filter="Disease"="Asthma"` returns studies tagged with that disease.

To include unpublished studies visible only to curators, use the curator path instead: `GET /api/v1/as-curator/studies`.

## Retrieve a single study by accession

When you already know a study's Genestack accession, send `GET /api/v1/as-user/studies/{id}` with the accession (for example, `GSF1102568`) to retrieve its metadata directly.

## Find samples matching metadata

Send `GET /api/v1/as-user/samples` with a `filter` parameter to retrieve samples matching specific metadata criteria, such as all samples of a given tissue type or organism.

## Run a full-text search across a study and its linked data

To search across everything linked to a study (the study metadata itself plus linked samples, libraries, preparations, and omics metadata), send `POST /api/v1/integration/fulltext/search/studies` with a JSON body. Typical goals:

- Find every study where a term such as "cancer" appears anywhere in the linked data.
- Find studies by a facet value, such as `"Disease" = "Asthma"` (the search covers only the facets defined in the Configure Facets application).

The response lists matching studies with their metadata summaries, together with facet objects and counts, the same facets shown in the Study Browser. The endpoint is ontology-aware: it automatically expands queries to include synonyms and child terms from configured ontologies.

## Next steps

To query *within* the studies you find (for example, to retrieve expression or variant data linked to them), see [Search imported data](search-imported-data.md) and [Cross-product queries](cross-product-queries.md).
