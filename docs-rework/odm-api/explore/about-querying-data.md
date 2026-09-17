---
diataxis: explanation
tab: odm-api
---

# About querying data

This page explains how data is organised for API access in ODM: what you can query, the two families of endpoints for retrieving it, and how endpoints are grouped by access path. For the concrete endpoints and parameters, follow the how-to guides linked throughout.

## What's queryable

From an API perspective, data in ODM falls into two categories.

**Indexed data** includes Expression, Variants, Flow Cytometry, and Tabular Data. This data is content-indexed on import, so you can query it by runs, values, metadata, or parent group metadata. HDF5 files are a special case: their structure is indexed so their contents can be parsed and browsed, but the values themselves are not content-indexed.

**Attached files** include PDFs, archives, and other non-indexed formats. Because their contents are not indexed, you can query them by metadata only, and they follow a different API workflow from indexed data: they cannot be accessed via the omics endpoints.

## Search vs. stream endpoints

ODM provides two families of endpoints for retrieving data, suited to different purposes.

**Search endpoints** return JSON containing metadata and values. They are cursor-paginated and suited to interactive exploration, exact lookups, and integrations that process structured JSON.

**Stream endpoints** return tab-delimited output and are designed for bulk export and downstream analysis. See [How to stream data exports](stream-data-exports.md).

## How endpoints are organised

Query endpoints are grouped by the access path they sit under, which determines both who can call them and what data they return:

- **`as-user/`** endpoints are available to all authenticated users and return published data.
- **`as-curator/`** endpoints require Curator group membership and additionally return unpublished data.
- **`manage-data/`** endpoints require the "Manage organisation" and "Access all data" permissions.

Within the `as-user/` and `as-curator/` paths, endpoints come in two flavours: **omics endpoints**, which query a single data type (expression, variant, flow cytometry, and so on), and **integration endpoints**, which query across linked entity types (for example, retrieving the samples linked to a library). For the omics endpoints and their filters, see [Search imported data](search-imported-data.md); for the integration endpoints, see [Cross-product queries](cross-product-queries.md). For the filter-expression language and query parameters shared across all of these, see [Query and filter syntax reference](../reference/query-and-filter-syntax-reference.md).

## Response format

Since release 1.58, search endpoints return data in the `multi_values` format by default, which supports one or more features per item and works for all tabular data types including GCT files. For the full response structure and the field changes this introduced, see [Response format changes reference](../reference/response-format-changes-reference.md).

For cell-level metadata specifics, see the [Cell analytics](cell-analytics/about-cell-analytics.md) section.
