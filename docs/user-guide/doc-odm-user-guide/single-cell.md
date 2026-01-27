Single Cell data refers to molecular measurements obtained from individual cells, rather than bulk samples where 
signals are averaged across many cells. This approach allows researchers to study the heterogeneity within a 
cell population, uncovering differences in gene expression, epigenetic states, or protein abundance between cells.

ODM now supports the Cell entity to store and manage metadata and expression for individual cells in Single Cell datasets.
Each cell record belongs to a Cell Group, which represents a single cell table (group).

## Cell metadata and Cell expression in ODM
Cell metadata can be imported into ODM using the `job` endpoints and [import_ODM_data script](../../tools/odm-sdk/terminal/study/uploading-study.md). 
Only TSV file format is supported to upload cell metadata.

### Uploading via API endpoints

Let's upload a new Study with Samples, Cell metadata, and Cell expression. For data import, you should go to the `job` 
section and choose the endpoint relevant for the specific data type.

In this example we will upload the following files:

[Study_metadata](https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/study_metadata.tsv),
a tab-delimited file of the study attributes:

| Study Source | Study Source ID | Study Title                         |
|--------------|-----------------|-------------------------------------|
| S3           | EXP_S_9988      | Single Cell Expression Data Search  |

Import study as [described here](../doc-odm-user-guide/import-data-using-api.md/#import-study).

[Samples_metadata](https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/samples.tsv),
a tab-delimited file of sample attributes:

| Sample Name | Sample Source ID | Sample Source | Sex    | Age | Cell Type   | Disease  |
|-------------|------------------|---------------|--------|-----|-------------|----------|
| EXP_SN_8801 | EXP_SSID_8801    | S3            | female | 28  | EXP_CT_8801 | diabetes |
| EXP_SN_8802 | EXP_SSID_8802    | S3            | male   | 29  | EXP_CT_8802 | melanoma |
| ...         | ...              | ...           | ...    | ... | ...         | ...      |

Import samples as [described here](../doc-odm-user-guide/import-data-using-api.md/#import-samples).

[Cell_metadata](https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/cells_2_samples_full_match.tsv),
a tab-delimited file of cell attributes:

| barcode        | sample_id     | cell_type  | treatment  | protocol    | cluster            | n_counts | percent_mito  | umap       | pca      | n_genes | doublet_scores | donor   | organ   | sort    | method | file            | assay      | disease  | organism      | sex    | development_stage |
|----------------|---------------|------------|------------|-------------|--------------------|----------|---------------|------------|----------|---------|----------------|---------|---------|---------|--------|-----------------|------------|----------|---------------|--------|-------------------|
| SMPL_CID_A1 01 | EXP_SSID_8801 | CD4_T_cell | stimulated | Smart-seq2  | Activated T cells  | 12500    | 0.8           | -1.2,2.5   | 1.8,-0.7 | 2800    | 0.05           | DONOR_A | spleen  | FACS_A  | scRNA  | SampleFile_A101 | Smart-seq2 | healthy  | Homo sapiens  | female | adult             |
| SMPL_CID_A102  | EXP_SSID_8802 | NK_cell    | resting    | Smart-seq2  | Resting NK_cells   | 8900     | 1.1           | 2.3,-1.8   | -0.9,2.1 | 2100    | 0.08           | DONOR_A | blood   | FACS_A  | scRNA  | SampleFile_A102 | Smart-seq2 | healthy  | Homo sapiens  | male   | adult             |
| SMPL_CID_A103  | EXP_SSID_8803 | CD4_T_cell | stimulated | Smart-seq2  | Memory T cells     | 15200    | 0.9           | -2.1,1.7   | 0.6,-1.9 | 3200    | 0.04           | DONOR_A | spleen  | FACS_A  | scRNA  | SampleFile_A103 | Smart-seq2 | healthy  | Homo sapiens  | female | adult             |
| SMPL_CID_A104  | EXP_SSID_8804 | CD8_T_cell | cytotoxic  | Smart-seq2  | Cytotoxic T cells  | 11800    | 1.2           | 1.9,-2.4   | -1.5,0.8 | 2900    | 0.07           | DONOR_A | blood   | FACS_A  | scRNA  | SampleFile_A104 | Smart-seq2 | healthy  | Homo sapiens  | male   | adult             |
| SMPL_CID_A105  | EXP_SSID_8805 | CD8_T_cell | resting    | Smart-seq2  | Naive CD8_T_cells  | 9300     | 1.0           | -0.8,1.3   | 2.2,-1.1 | 2500    | 0.06           | DONOR_A | spleen  | FACS_A  | scRNA  | SampleFile_A105 | Smart-seq2 | healthy  | Homo sapiens  | female | adult             |


For Cell metadata use the following endpoints:

* Supply the file URL via dataLink

    **Path:** POST `/api/v1/jobs/import/cells`

* Upload directly from TSV file 

    **Path:** POST `/api/v1/jobs/import/cells/multipart`

[Cell_expression](https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/expression_2_cells_linked_to_samples.tsv),
  a tab-delimited file of cell expression data:

| gene_id          | SMPL_CID_A101 | SMPL_CID_A102 | SMPL_CID_A103 | SMPL_CID_A104 | SMPL_CID_A105 |
|------------------|---------------|---------------|---------------|---------------|---------------|
| ENSG00000230368  | 1.01          | 1.02          | 1.03          | 1.04          | 1.05          |
| ENSG00000188976  | 2.01          | 2.02          | 2.03          | 2.04          | 2.05          |
| ACTB             | 3.01          | 3.02          | 3.03          | 3.04          | 3.05          |

For Cell expression use the following endpoints:

* Supply the file URL via dataLink

    **Path:** POST `/api/v1/jobs/import/expression`

* Upload directly from TSV file

    **Path:** POST `/api/v1/jobs/import/expression/multipart`
    
    **It is recommended to use TSV files archived in `.br` or `.lz4` extensions for Cell expression.**

When the import job finishes successfully, the resulting Group accession can be retrieved with the following endpoint:  
GET `/api/v1/jobs/{jobExecId}/output`.

Example response:
```json
{
"groupAccession": "GSF1234567"
}
```
Learn more about [uploading data to ODM via API here](../doc-odm-user-guide/import-data-using-api.md).

### Uploading via script

Curators can upload and link Cell metadata groups to ODM using the [import_ODM_data script](../../tools/odm-sdk/terminal/study/uploading-study.md).
This extension allows you to include Cell groups in the same import workflow as other metadata entities (Studies, 
Samples, Libraries, and Preparations), ensuring a consistent and automated data-loading process.

#### Parameters

The script supports optional parameter for Cell metadata: `-c` `--cell`

| Feature              | Description                                      |
| -------------------- | ------------------------------------------------ |
| **Parameter**        | `--cell` / `-c`                                  |
| **Input format**     | TSV (same format as `/api/v1/jobs/import/cells`) |
| **Linking targets**  | Samples, Libraries, or Preparations              |
| **Multiple imports** | Supported in one run                             |
| **Error handling**   | Aligned with Cell import endpoint                |

For uploading Cell expression please use regular `-e` `--expression` parameters.

#### Supported Import Scenarios

Cells can be imported and linked in several hierarchical contexts, depending on your dataset structure. There are few examples:

1. **Study → Samples → Cells → Expression** 

    Used when cells are directly associated with samples.

2. **Study → Samples → Library → Cells → Expression** / **Study → Samples → Preparation → Library → Cells → Expression**

    Used when cells originate from library-level data.

3. **Study → Samples → Preparations → Cells → Expression** / **Study → Samples → Library → Preparation → Cells → Expression**

    Used when cells originate from preparation-level data.

Note that Cell metadata will be linked to the nearest metadata group mentioned above in the script.

#### Script example

```
odm-import-data \
--server <HOST> \
--token <HOST> \
--study 's3://bio-test-data/User_guide_test_data/Single_cell_data/study_metadata.tsv' \
--samples 's3://bio-test-data/User_guide_test_data/Single_cell_data/samples.tsv' \
--cells 's3://bio-test-data/User_guide_test_data/Single_cell_data/cells_2_samples_full_match.tsv' \
--expression 's3://bio-test-data/User_guide_test_data/Single_cell_data/expression_2_cells_linked_to_samples.tsv' \
--data-class 'Single-cell transcriptomics' \
--number-of-feature-attributes 1 \
--allow-duplicates
```

### Common rules for TSV files with Cell metadata

#### Stored attributes and limitations
There is the list of values parsed and stored within the system. 

All other values presented in Cell metadata file will be stored as custom attributes with string data type.

| Attribute Name | Stored as type | Description                                                                                                  | Required |
|----------------|----------------|--------------------------------------------------------------------------------------------------------------|----------|
| cellID         | string         | Unique cell identifier generated by ODM (composite key of `groupAccession` + `barcode`)                      | Yes      |
| barcode        | string         | Raw cell barcode. **Must be unique**.                                                                        | Yes      |
| batch          | string         | Sample/batch origin                                                                                          | Yes      |
| cellType       | string         | Annotated cell type                                                                                          |          |
| cluster        | string         | Clustering labels                                                                                            |          |
| nCounts        | integer        | Total UMI count (Unique Molecular Identifier)                                                                |          |
| percentMito    | float          | % mitochondrial gene expression                                                                              |          |
| umap           | float          | Dimensionality reduction results (Uniform Manifold Approximation and Projection). Up to 3 values are stored. |          |
| pca            | float          | Dimensionality reduction results (Principal Component Analysis results). Up to 100 values are stored.        |          |
| tsne           | float          | Up to 3 values are stored.                                                                                   |          |

#### Validation

Fail conditions:

* Missing required attributes (`barcode`, `batch`)
* Duplicate barcodes within a group 
* Blank values in required attributes

Warnings (ignored values):

* Invalid data type for attribute

### Linking Cell metadata to Samples, Libraries, Preparations

#### Common rules

To link Cell metadata to other metadata groups use the following endpoints: 

**Swagger definition:** `integrationCurator` → `Cell integration as Curator`

* Link to Samples

    **Path:** POST `/api/v1/as-curator/integration/link/cell/group/{sourceId}/to/sample/group/{targetId}`

* Link to Libraries

    **Path:** POST `/api/v1/as-curator/integration/link/cells/group/{sourceId}/to/library/group/{targetId}`

* Link to Preparations

    **Path:** POST `/api/v1/as-curator/integration/link/cells/group/{sourceId}/to/preparation/group/{targetId}`

For `sourceId` field provide accession of your Cell metadata group.
For `targetId` field provide accession of selected Sample, Library, or Preparation group where Cell metadata should be linked.

Cell metadata will be linked if there are matches between `batch` values in Cell metadata and `Sample Source ID` for Samples,
`Library ID` for Libraries, and `Preparation ID` for Preparations. 

#### Validation

Fail conditions: 

* There is no Sample Source/Library/Preparation ID in Sample/Library/Preparation metadata group.
* There are no matches between `batch` in Cell metadata and Sample Source/Library/Preparation IDs.

The amount of successfully created links between Cells and Samples/Libraries/Preparations will be shown in response 
message if linkage is successful.

### Linking Cell expression to Cell metadata

To link Cell expression to Cell metadata group use the following endpoint:

**Swagger definition:** `integrationCurator` → `Expression integration as Curator`

**Path:** POST `/api/v1/as-curator/integration/link/expression/group/{sourceId}/to/cell/group/{targetId}`

For `sourceId` field provide accession of your Cell expression group.

For `targetId` field provide accession of selected Cell metadata group which Cell expression should be linked to.

A Cell expression group can be linked to one Cell metadata group only.

## [BETA] Analytics

### Cell ratio
Compute cell ratio statistics across groups or metadata attributes in single-cell data.
This endpoint calculates cell ratio statistics based on single-cell metadata. 
It quantifies the proportion of cells that meet specific criteria (`countSelected`, e.g., expression 
threshold, cell type, or cluster) relative to a defined reference group or the total cell population 
(`countAvailable`) defined by study, samples, library, or preparation metadata.

**Swagger definition:** `integrationCurator` → `[BETA] Analytics omics queries as Curator`

**Path:** POST `/api/v1/as-curator/omics/cells/analytics/cell-ratio`

The Cell Ratio endpoint computes a simple proportion:

* `countSelected` = number of cells that match all provided criteria (study/sample/library/preparation + cell metadata + optional expression constraints)
* `countAvailable` = number of cells in the reference population defined **only** by study/sample/library/preparation queries & filters 
* `ratio` = `countSelected` / `countAvailable`

This endpoint returns **counters only** (no cell records).

Use it when you want to answer questions like:

* “What fraction of cells in `Study X` are `Monocytes`?” 
* “Within samples matching `Clozapine`, what proportion of cells have expression in a given range?” 
* “Among cells from a specific library/preparation, what fraction match a cell metadata definition?”

Request example:
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
Response example:
```json
{
  "countSelected": 1243393,
  "countAvailable": 9234945,
  "ratio": 0.13465
}
```
### Gene summary
The Gene Summary endpoint returns **descriptive statistics and distribution summaries** for expression values of up to 
**100 genes** across a filtered set of single cells.

You use it when you want quick “what does this gene look like in these cells?” metrics: 
mean/median, spread, quantiles, min/max, and a histogram-style density summary.

**Swagger definition:** `integrationCurator` → `[BETA] Analytics omics queries as Curator`

**Path:** POST `/api/v1/as-curator/omics/cells/analytics/gene-summary`

For each requested gene, the response includes:

* `geneId`: gene identifier (e.g., Ensembl ID)
* `cellCount`: number of cells with measurable expression for the gene under the applied filters 
* `mean`: average expression value 
* `median`: median expression value 
* `stdDev`: standard deviation (dispersion)
* `min` / `max`: observed range of expression values 
* `quantiles`: expression percentiles (configurable set of percentiles; returned as an ordered list of values)
* `histogram` (density): binned distribution summary suitable for plotting expression density

Request example:
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
  "geneNames": [
    "ENSG00000230368",
    "ENSG00000188976",
    "ENSG00000188982"
  ],
  "exQuery": "-3 < value < 3"
}
```
Response example:
```json
{
  "resultsPerGene": [
    {
      "geneId": "ENSG00000111640",
      "cellCount": 8968167,
      "mean": 7.747614311820911,
      "median": 7,
      "stdDev": 6.499314669429827,
      "min": 1,
      "max": 496,
      "quantiles": [
        1,
        1,
        2,
        3,
        5,
        7,
        10,
        12,
        15,
        27,
        192
      ],
      "histogram": "[(1, 15.50289002318, 7686678.375), (15.50289002318, 35.49570418233824, 1229164),\n(35.49570418233824, 56.93121325335453, 36531.25), (56.93121325335453, 77.21467372919479, 6910.625)]\n"
    }
  ]
}
```

### Differential expression
The Differential Expression endpoint compares gene expression between two cell populations: 
a `Case` group and a `Control` group. It returns per-gene metrics that quantify how strongly expression
differs between the two groups, including **fold change** and **Mann–Whitney U test** results.

**Swagger definition:** `integrationCurator` → `[BETA] Analytics omics queries as Curator`

**Path:** POST `/api/v1/as-curator/omics/cells/analytics/differential-expression`

Use it to answer questions like:

* “Which genes are upregulated in `Monocytes` vs all other cells?” 
* “Which genes differ between case samples and control samples within the same study?” 
* “What changes under a treatment condition vs untreated controls?”

Calculations for each returned `geneId`:

* `caseCellCount`: number of case cells contributing measurable expression for that gene 
* `controlCellCount`: number of control cells contributing measurable expression for that gene 
* `caseAvgEx`: mean expression across contributing case cells 
* `controlAvgEx`: mean expression across contributing control cells 
* `expressionDifference`: `caseAvgEx` - `controlAvgEx` 
* `foldChange`: `caseAvgEx` / `controlAvgEx` 
* `mannWhitneyU` / `pValue`: Mann–Whitney U test outputs (as implemented by ClickHouse mannwhitneyutest)
* `log2FC`: the fold change expressed on a base-2 logarithmic scale

If you apply exQuery expression thresholds, only cells/expression values that satisfy those rules contribute to the counts and averages.

Request example:
```json
{
  "caseGroup": {
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
  "controlGroup": {
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
  "exQuery": "feature=ENSG00000230368,ENSG00000188976",
  "limit": 2000,
  "offset": 0
}
```
Response example:
```json
{
  "resultsPerGene": [
    {
      "geneId": "ENSG00000230368",
      "caseCellCount": 8450,
      "controlCellCount": 8123,
      "caseAvgExpression": 1.24,
      "controlAvgExpression": 0.62,
      "expressionDifference": 0.62,
      "foldChange": 2,
      "mannWhitneyU": 1.5,
      "pValue": 0.95
    }
  ],
  "pagination": {
    "currentResultsCount": 1,
    "limit": 2000,
    "offset": 0
  }
}
```

## Delete Cell metadata and Cell expression

Please use [manage-data/data endpoint](../../user-guide/quick-start/admin-api.md/#use-case-example-delete-data-in-odm) to delete Cell metadata or Cell expression group.
