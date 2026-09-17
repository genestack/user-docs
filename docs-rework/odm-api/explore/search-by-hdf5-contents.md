---
diataxis: how-to
tab: odm-api
---

# How to search by HDF5 file contents

This guide shows you how to find HDF5 files, and the studies linked to them, by the internal structure of the files rather than by metadata.

For the full list of structural query parameters, see the [HDF5 structural queries](../reference/query-and-filter-syntax-reference.md#hdf5-structural-queries) section of the syntax reference. For the complete parameters and response schema of any endpoint, see the [Swagger UI](/swagger/helper/).

## Prerequisites

- An API token. See [Authentication and tokens](../getting-started/authentication-and-tokens.md).
- The studies containing the HDF5 files must be shared with you, or you must have the "Access all data" permission.
- HDF5 files are detected by their `.h5` or `.h5ad` extension on import, and their structure is parsed and stored in ODM at that time.

## Find HDF5 files by internal structure

Send `GET /api/v1/as-user/files` (or `as-curator`) with one or more structural query parameters (`fullPath`, `partialPath`, `group`, or `dataset`) to find files whose internal structure matches. Add `includeContents=true` to return the parsed structure alongside the file metadata.

For example, `group=obsm` and `dataset=seurat_clusters` find files containing that dataset within that group.

## Find studies by linked HDF5 file structure

To find the studies linked to matching files, send `GET /api/v1/as-user/integration/link/studies/by/files` (or `as-curator`) with the same structural parameters.

## Response structure

When `includeContents=true`, the response includes the parsed file structure: groups, datasets, files, folders, and h5 pairs. If parsing fails, the contents section reports the error instead:

```json
"contents": {"error": "The contents could not be parsed."}
```

When `includeContents=false` (the default), the contents section is omitted and only file metadata and accession are returned.

For context on what HDF5 files contain and how single-cell data is stored in ODM, see [Supported data formats](../../overview/supported-data-formats/index.md). To search attached files by metadata rather than structure, see [Search attached files](search-attached-files.md).
