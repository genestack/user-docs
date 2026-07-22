---
diataxis: how-to
tab: odm-api
---

# How to stream data exports

This guide shows you how to retrieve large datasets from ODM as streamed, tab-delimited output.

For the filter and streaming parameters, see [Query and filter syntax reference](../reference/query-and-filter-syntax-reference.md). For the complete parameters and response schema of any endpoint, see the [Swagger UI](/swagger/helper/).

## When to use streaming endpoints

Use streaming endpoints when you need an entire dataset (or a filtered subset of it) rather than paginated JSON. Streaming avoids the overhead of JSON encoding and the complexity of managing many pages of results, making it the right choice for bulk exports and downstream analysis pipelines. For paginated JSON instead, see [Search imported data](search-imported-data.md).

## Stream a data type

ODM provides streaming endpoints for the three main indexed data types, each with a user and a curator path:

- **Expression:** `GET /api/v1/as-user/omics/expression/streamed-data` (or `as-curator`)
- **Variant:** `GET /api/v1/as-user/omics/variant/streamed-data` (or `as-curator`)
- **Flow cytometry:** follows the same pattern.

An unfiltered request returns the complete dataset. To narrow it, streaming endpoints accept the same filter parameters as their non-streaming counterparts (`exFilter`/`exQuery`, `vxFilter`/`vxQuery`, `runFilter`, `metadataFilter`). See the [syntax reference](../reference/query-and-filter-syntax-reference.md#query-parameters-by-data-type).

## Combine variant and expression data in one call

The variant streaming endpoints also accept the `exQuery` parameter, which restricts the variant output to samples linked to expression data meeting the specified expression criteria. This lets you run integrated expression-and-variant analysis in a single streaming call.

## Consume the stream

Streaming responses are returned as tab-delimited text. Consume them as a stream in your client rather than buffering the whole response:

- **curl:** `curl -o output.tsv "https://<HOST>/api/v1/as-user/omics/expression/streamed-data?..." -H "Genestack-API-Token: <TOKEN>"`
- **Python:** use `requests` in streaming mode (`stream=True`)
- **R:** use a streaming-compatible HTTP client

To control numeric precision in the output, use the `roundDigits` parameter (default `4`).
