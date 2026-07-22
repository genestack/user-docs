---
diataxis: reference
tab: odm-api
---

# Query and filter syntax reference

This reference describes the query language and shared parameters used across the ODM Explore API endpoints: filter expressions, URL-encoding, pagination, and the query parameters that recur across data types. It does not list endpoints or their full schemas. The [Swagger UI](/swagger/helper/) is the canonical source for endpoint paths, parameters, and response schemas.

## Filter expressions

Metadata filters are written as attribute-name/value expressions:

```
"AttributeName" = "value"
```

- **Wildcards:** `?` matches a single character; `*` matches any number of characters.
- **Logical operators:** `AND`, `OR`, and `NOT`. `OR` is the default when combining terms.
- **`filter`** filters by metadata attribute values; **`query`** performs a keyword search across metadata.

## URL-encoding

Filter values passed in a query string must be URL-encoded. For example:

- `?filter=%22Library%20ID%22%3D%20LIB1` decodes to `"Library ID"= LIB1`
- `?filter=%22Sample%20Source%20ID%22%20%3D%20HG00119` decodes to `"Sample Source ID" = HG00119`

## Pagination

Two pagination styles are used across the Explore API:

- **Offset-based:** `pageOffset` and `pageLimit` control the window of results (studies and samples).
- **Cursor-based:** large result sets return a `cursor` value; pass it on the next request to retrieve the following page.

## Query parameters by data type

The [Swagger UI](/swagger/helper/) lists the complete parameter set for every endpoint. The parameters below recur across the Explore API and carry ODM-specific semantics worth documenting in one place.

### Expression data

- `exFilter`, filter by expression object metadata (for example, `genestack:accession = GSF1283537`)
- `exQuery`, filter by feature or measurement values (for example, `feature.Genes="ZNF814"`, `value.intensity > A`)

### Variant data

- `vxFilter`, filter variants by metadata attributes
- `vxQuery`, compound filter expressions using logical operators: not (`!`), and (`&&`), or (`||`)
- `variantFeature` (release 1.59+), filter by gene name. ODM resolves the gene to genomic intervals via the associated reference genome and returns all variants within those intervals. Accepts a string array of gene symbols (for example, `TP53`) and matches gene names exactly.
- `variantInfo` (release 1.59+), filter by exact match on VCF INFO field values:
    - `info.key=value`, return variants where the INFO field matches exactly
    - `info.key!=value`, exclude variants with that value
    - `exists(INFO.KEY)` / `!exists(INFO.KEY)`, return variants that have / do not have the specified INFO key
    - multiple comma-separated values for a key are treated as OR conditions
- `referenceGenomeId` (release 1.59+), filter variant groups by Reference Genome ID (on `.../omics/variant/group` and the curator equivalent)

### Flow cytometry data

Flow cytometry endpoints follow the same filter pattern as expression and variant data.

### Common parameters

- `runFilter`, filter by Genestack-generated internal run IDs (accepts a list of strings)
- `runSourceFilter`, filter by run IDs from the original files
- `metadataFilter`, filter by object-level metadata

### HDF5 structural queries

Filter attached HDF5 files by their parsed internal structure:

- `fullPath`, exact full path within the file (for example, `/obs/__categories/integrated_snn_res.0.5`)
- `partialPath`, partial path (for example, `__categories/integrated_snn_res.0.5`)
- `group`, group name (for example, `obsm`)
- `dataset`, dataset name (for example, `seurat_clusters`)
- `includeContents`, include the parsed contents object in the response (default `false`)

### Streaming

- `roundDigits`, number of decimal digits for numeric values in streamed output (default `4`)

Streaming endpoints accept the same filter parameters as their non-streaming counterparts.

## Response format

Search endpoints return a `data` array in the `multi_values` format (the default since release 1.58). For the full field-by-field response structure and the changes that format introduced, see [Response format changes reference](response-format-changes-reference.md).

## Related

- [About querying data](../explore/about-querying-data.md)
- [Swagger orientation](../getting-started/swagger-orientation.md)
