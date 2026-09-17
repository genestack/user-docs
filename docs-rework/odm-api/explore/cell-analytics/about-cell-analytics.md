---
diataxis: explanation
tab: odm-api
---

# About Cell analytics

> **[BETA]** The Cell analytics endpoints described here are in BETA as of release 1.62 and are subject to change.

Cell analytics is a set of API endpoints that compute statistics over single-cell data. Each endpoint accepts one or more cohort definitions (filters that select a subset of cells based on study, sample, library, preparation, and cell-metadata criteria, optionally combined with expression constraints) and returns aggregate results for those cohorts.

## The three endpoints

All three endpoints live in the `integrationCurator` Swagger definition under **[BETA] Analytics omics queries as Curator**.

**Cell Ratio** (`POST /api/v1/as-curator/omics/cells/analytics/cell-ratio`) computes the proportion of cells matching criteria. The endpoint returns:

- `countSelected`, number of cells matching all provided criteria
- `countAvailable`, number of cells in the reference population defined by the study/sample/library/preparation filters alone
- `ratio`, `countSelected` divided by `countAvailable`

This endpoint returns counters only, no individual cell records.

**Gene Summary** computes descriptive statistics (mean, median, standard deviation, quantiles, histogram) for up to 100 genes across the filtered cell population.

**Differential Expression** performs a case-versus-control comparison, returning fold change values and Mann-Whitney U test results for genes that differ between two cohort groups.

## Common request shape

All three endpoints share a common request pattern. A `cellGroup` object specifies the cohort using filters and queries across the entity hierarchy:

```json
{
  "cellGroup": {
    "studyFilter": "\"Study Source\"=ArrayExpress",
    "studyQuery": "RNA-Seq of human dendritic cells",
    "sampleFilter": "\"Species or strain\"=\"Homo sapiens\"",
    "sampleQuery": "Clozapine",
    "libraryFilter": "\"Library Type\"=RNA-Seq-1",
    "libraryQuery": "illumina HiSeq500",
    "preparationFilter": "Digestion=Trypsin",
    "preparationQuery": "reversed-phase liquid chromatography",
    "cellQuery": "cellType=Macrophage,Monocyte",
    "searchSpecificTerms": false
  },
  "exQuery": "-3 < value < 3"
}
```

Cell Ratio and Gene Summary accept a single `cellGroup`. Differential Expression accepts two: `caseGroup` and `controlGroup`.

## When to use each endpoint

Use **Cell Ratio** when you want to answer questions like: "What fraction of cells in Study X are Monocytes?" or "Among cells from a specific library, what proportion match a given definition?"

Use **Gene Summary** when you need a quick distribution snapshot for a gene in a defined cell population: "What does this gene look like in these cells?"

Use **Differential Expression** when you want to identify which genes differ between two cell cohorts: "Which genes differ between case and control cells?"

For the full request and response schemas, see the Swagger definition or the [Cell analytics reference](cell-analytics-reference.md).
