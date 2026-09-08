---
diataxis: explanation
tab: odm-api
---

# API Reference

Swagger already documents every ODM endpoint, along with its parameters and schemas, so this section does not repeat that. What it collects instead are the cross-cutting details that no single endpoint owns: the query language you write filters in, the shape of the data you get back, and the conventions that hold across the API. When you need to understand how something works across the whole API rather than what one endpoint returns, start here. For navigating Swagger itself, see [Swagger orientation](../getting-started/swagger-orientation.md).

## Reference pages

<div class="grid cards gs-section-cards" markdown>

- __[Query and filter syntax reference](query-and-filter-syntax-reference.md)__

    ---

    The filter-expression language, URL-encoding, pagination, and the query parameters shared across the Explore API.

- __[Cell metadata reference](cell-metadata-reference.md)__

    ---

    Attributes, data types, required fields, and validation rules for Cell metadata TSV files.

- __[Job status codes reference](job-status-codes-reference.md)__

    ---

    The `jobExecId` lifecycle, status values, and file-type-specific behaviour for import jobs.

- __[Response format changes reference](response-format-changes-reference.md)__

    ---

    The `multi_values` format, `itemOrigin`, and `feature`/`value` sections introduced in release 1.58.

</div>
