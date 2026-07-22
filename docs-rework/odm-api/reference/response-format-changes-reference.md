---
diataxis: reference
tab: odm-api
---

# Response format changes reference

Release 1.58 introduced significant response format changes for GET endpoints that return data in JSON format: Tabular (including GCT/expression), Variant, and Flow Cytometry. The new `multi_values` format became the default. The older format is deprecated.

Streaming GET endpoints that return output in tabular text format are not affected. See [How to stream data exports](../explore/stream-data-exports.md).

---

## Common changes for all data types

The following changes apply to all affected endpoints:

| Change | Description |
|---|---|
| New `itemOrigin` section | A new section in the response body stores origin metadata: `runSourceId` (run ID from the original file), `runId` (Genestack-generated internal run ID), `groupId` (ID of the original file). |
| `Run Source ID` moved | The `Run Source ID` field has been moved from the `metadata` section to `itemOrigin` and renamed to `runSourceId`. In OMICS endpoints, `sampleFilter`, `libraryFilter`, or `preparationFilter` can be used to retrieve an individual run. |
| New `runSourceFilter` parameter | Filters data by Run IDs from original files. |
| `runFilter` takes list of strings | The `runFilter` parameter, which accepts auto-generated internal run IDs, now takes a list of strings. |
| Deprecated filter option | Filtering by `Run Source ID` in the metadata filter is no longer available. |

### Affected endpoints (common changes)

Both `as-curator` and `as-user` variants are affected:

- `GET /api/v1/as-user/expressions`, `GET /api/v1/as-user/expressions/{id}`
- `GET /api/v1/as-curator/expressions`, `GET /api/v1/as-curator/expressions/{id}`
- `GET /api/v1/as-user/variants`, `GET /api/v1/as-user/variants/{id}`
- `GET /api/v1/as-curator/variants`, `GET /api/v1/as-curator/variants/{id}`
- `GET /api/v1/as-user/flow-cytometries`, `GET /api/v1/as-user/flow-cytometries/{id}`
- `GET /api/v1/as-curator/flow-cytometries`, `GET /api/v1/as-curator/flow-cytometries/{id}`
- `GET /api/v1/as-user/omics/expression/data`, `GET /api/v1/as-user/omics/variant/data`, `GET /api/v1/as-user/omics/flow-cytometry/data`
- `GET /api/v1/as-curator/omics/expression/data`, `GET /api/v1/as-curator/omics/variant/data`, `GET /api/v1/as-curator/omics/flow-cytometry/data`

---

## Tabular data endpoint changes

| Change | Description |
|---|---|
| Old response format deprecated | The old response format for tabular data is deprecated. The `multi_values` response format (introduced July 2023) is now the default. It supports data with one or more features and works for any tabular data type including `.gct` files. |
| Field rename: `gene` → `feature` | The `gene` field is renamed to `feature` and incorporates all feature attributes. |
| Field rename: `expression` → `value` | The `expression` field is renamed to `value` and placed in a new `value` section. |

### Affected endpoints (tabular data)

- `GET /api/v1/as-user/expressions`, `GET /api/v1/as-user/expressions/{id}`
- `GET /api/v1/as-curator/expressions`, `GET /api/v1/as-curator/expressions/{id}`
- `GET /api/v1/as-user/omics/expression/data`
- `GET /api/v1/as-curator/omics/expression/data`

---

## Variant endpoint changes

| Change | Description |
|---|---|
| New `variant` section | A new `variant` section contains all fields related to a specific variation from the original VCF file: `CHROM`, `POS`, `ID`, `REF`, `ALT`, `QUAL`, `FILTER`, `INFO`. |

### Affected endpoints (variants)

- `GET /api/v1/as-user/variants`, `GET /api/v1/as-user/variants/{id}`
- `GET /api/v1/as-curator/variants`, `GET /api/v1/as-curator/variants/{id}`
- `GET /api/v1/as-user/omics/variant/data`
- `GET /api/v1/as-curator/omics/variant/data`

---

## Flow cytometry endpoint changes

| Change | Description |
|---|---|
| New `feature` section | The `feature` section contains `readoutType`, `cellPopulation`, and `marker` fields. |
| `expression` renamed to `value` | The `expression` field is renamed to `value` and placed in a new `value` section. |

### Affected endpoints (flow cytometry)

- `GET /api/v1/as-user/flow-cytometries`, `GET /api/v1/as-user/flow-cytometries/{id}`
- `GET /api/v1/as-curator/flow-cytometries`, `GET /api/v1/as-curator/flow-cytometries/{id}`
- `GET /api/v1/as-user/omics/flow-cytometry/data`
- `GET /api/v1/as-curator/omics/flow-cytometry/data`

---

## Backward compatibility

The old `responseFormat` value still functions but is deprecated. Update integrations to use `multi_values`, which is now the default since release 1.58.

## Related

- [About querying data](../explore/about-querying-data.md)
- [Search imported data](../explore/search-imported-data.md)
- [How to stream data exports](../explore/stream-data-exports.md)
