---
diataxis: reference
tab: odm-api
---

# Cell analytics reference

> **[BETA]** These endpoints are in BETA as of release 1.62 and are subject to change.

All three Cell analytics endpoints live in the `integrationCurator` Swagger definition under **[BETA] Analytics omics queries as Curator**. All require Curator group membership.

## Shared request fields

Every Cell analytics endpoint accepts a cohort filter object (`cellGroup`, `caseGroup`, or `controlGroup`) with the following fields:

| Field | Description |
|---|---|
| `studyFilter` | Filter by study metadata (e.g., `"Study Source"=ArrayExpress`) |
| `studyQuery` | Keyword search across study metadata |
| `sampleFilter` | Filter by sample metadata |
| `sampleQuery` | Keyword search across sample metadata |
| `libraryFilter` | Filter by library metadata |
| `libraryQuery` | Keyword search across library metadata |
| `preparationFilter` | Filter by preparation metadata |
| `preparationQuery` | Keyword search across preparation metadata |
| `cellQuery` | Filter by cell metadata (e.g., `cellType=Macrophage,Monocyte`) |
| `searchSpecificTerms` | Boolean; when `true`, disables ontology expansion |

The `exQuery` field is a top-level parameter (not inside the cohort object) that applies an expression filter to restrict which expression values contribute to the computation (e.g., `"-3 < value < 3"` or `"feature=ENSG00000230368,ENSG00000188976"`).

---

## Cell Ratio endpoint

**Path:** `POST /api/v1/as-curator/omics/cells/analytics/cell-ratio`

Computes the proportion of cells matching all criteria relative to a reference population.

**Request body:**

```json
{
  "cellGroup": { ... },
  "exQuery": "-3 < value < 3"
}
```

**Response fields:**

| Field | Description |
|---|---|
| `countSelected` | Number of cells matching all criteria (cohort filter + expression filter) |
| `countAvailable` | Number of cells in the reference population (study/sample/library/preparation filters only; no cell-metadata or expression filter) |
| `ratio` | `countSelected / countAvailable` |

**Example response:**

```json
{
  "countSelected": 1243393,
  "countAvailable": 9234945,
  "ratio": 0.13465
}
```

---

## Gene Summary endpoint

**Path:** `POST /api/v1/as-curator/omics/cells/analytics/gene-summary`

Returns descriptive statistics and distribution summaries for expression values of up to 100 genes across a filtered cell population.

**Request body:**

```json
{
  "cellGroup": { ... },
  "geneNames": ["ENSG00000230368", "ENSG00000188976", "ENSG00000188982"],
  "exQuery": "-3 < value < 3"
}
```

`geneNames` accepts up to 100 gene identifiers.

**Response fields per gene:**

| Field | Description |
|---|---|
| `geneId` | Gene identifier (e.g., Ensembl ID) |
| `cellCount` | Number of cells with measurable expression under the applied filters |
| `mean` | Average expression value |
| `median` | Median expression value |
| `stdDev` | Standard deviation |
| `min` | Minimum observed expression value |
| `max` | Maximum observed expression value |
| `quantiles` | Expression percentiles as an ordered list |
| `histogram` | Binned distribution summary as a list of `(bin_start, bin_end, count)` tuples |

---

## Differential Expression endpoint

**Path:** `POST /api/v1/as-curator/omics/cells/analytics/differential-expression`

Compares gene expression between a case group and a control group and returns per-gene statistical results.

**Request body:**

```json
{
  "caseGroup": { ... },
  "controlGroup": { ... },
  "exQuery": "feature=ENSG00000230368,ENSG00000188976",
  "limit": 2000,
  "offset": 0
}
```

`caseGroup` and `controlGroup` follow the same field structure as `cellGroup` above. `limit` and `offset` control pagination of the results.

**Response fields per gene:**

| Field | Description |
|---|---|
| `geneId` | Gene identifier |
| `caseCellCount` | Number of case cells with measurable expression |
| `controlCellCount` | Number of control cells with measurable expression |
| `caseAvgExpression` | Mean expression across case cells |
| `controlAvgExpression` | Mean expression across control cells |
| `expressionDifference` | `caseAvgExpression - controlAvgExpression` |
| `foldChange` | `caseAvgExpression / controlAvgExpression` |
| `mannWhitneyU` | Mann-Whitney U test statistic |
| `pValue` | Associated p-value |
| `log2FC` | Fold change on a base-2 logarithmic scale |

The response also includes a `pagination` block with `currentResultsCount`, `limit`, and `offset`.

> If an `exQuery` expression threshold is applied, only cells and expression values satisfying that threshold contribute to the counts and averages.
