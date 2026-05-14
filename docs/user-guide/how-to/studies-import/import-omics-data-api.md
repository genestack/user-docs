# Import omics data (API)

**Role:** Contributor

Prerequisites: you must have already imported a study and samples. See [Import samples (API)](import-samples-api.md).

> For a simpler GUI workflow for expression data, see [Import omics data (interface)](import-omics-data-gui.md).

## Signal Data Import

### Expression data

- [Test_expression.gct](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_expression.gct), a [GCT](https://software.broadinstitute.org/cancer/software/gsea/wiki/index.php/Data_formats#GCT:_Gene_Cluster_Text_file_format_.28.2A.gct.29) file of expression data from multiple sequencing runs. Note in this example the GCT file is using library IDs for linking.

| Name            | Description   |   LIB1 |   LIB2 |
|-----------------|---------------|--------|--------|
| ENSG00000077044 |               |   21.9 |   19.9 |
| ENSG00000085982 |               |   23.7 |   24.9 |

- [Test_generic_expression.tsv](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_generic_expression.tsv),  a tabular dataset in TSV (tab-separated values) format. 

| Text Feature One | Text Feature Two | Numeric Feature One | Numeric Feature Two | HG00119.m1 | HG00121.m1 | HG00183.m1 | HG00176.m1 |
|------------------|------------------|----------------------|----------------------|-------------|-------------|-------------|-------------|
| f1_1             | f2_1             | 1.069                | 2.218                | 0.804       | 0.350       | 0.591       | 7.260       |
| f1_2             | f2_2             | 4.845                | 0.391                | 0.729       | 5.657       |11.730       |11.007       |
| f1_3             | f2_3             | 1.427                | 0.147                | 1.588       | 8.145       | 1.480       | 2.718       |
| f1_4             | f2_4             | 4.854                | 3.723                | 0.645       | 4.493       | 0.862       | 1.370       |
| f1_5             | f2_5             |10.563                | 4.217                | 1.102       | 1.627       | 3.157       | 4.393       |


- [Test_generic_expression_lib.tsv](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_generic_expression_lib.tsv), a tabular dataset in TSV (tab-separated values) format. This file is structured to be **linked to Libraries**.

| Text Feature One | Text Feature Two | Numeric Feature One | Numeric Feature Two | LIB1.m1 | LIB2.m1 | LIB3.m1 |
|------------------|------------------|----------------------|----------------------|---------|---------|---------|
| f1_2             | f2_2             | 4.845                | 0.391                | 0.729   | 5.657   |11.730   |
| f1_3             | f2_3             | 1.427                | 0.147                | 1.588   | 8.145   | 1.480   |
| f1_4             | f2_4             | 4.854                | 3.723                | 0.645   | 4.493   | 0.862   |
| f1_5             | f2_5             |10.563                | 4.217                | 1.102   | 1.627   | 3.157   |


- [Test_expression.gct.tsv](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_expression.gct.tsv), a tab-separated file that describes the expression data.

| Normalization Method   | Genome Version   |
|------------------------|------------------|
| RPKM                   | GRCh38.91        |

#### Import process

This time, we're going to import expression data, supplying two files, one for the metadata, and another for the
processed data:

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/expression?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_expression.gct.tsv",
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_expression.gct",
  "dataClass": "Bulk transcriptomics"
}'
```
The example call in Swagger contain multiple additional fields, that we do not require to be able to import the data. In order to be able to load the data, we will only use *metadataLink*, *dataLink* and *dataClass*.

Alternatively, we can import the generic data file, which has features and dot separated measurements.
Please note, that in this example `numberOfFeatureAttributes` and `measurementSeparator` are mandatory. To learn more about this data type and mandatory fields please see [this page](../supported-formats/#tabular-data).

```default
curl -X 'POST' \
  'https://<TOKEN>/api/v1/jobs/import/expression?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_generic_expression.tsv",
  "numberOfFeatureAttributes": 4,
  "dataClass": "Proteomics",
  "measurementSeparator": "."
}'
```

!!! note "Data Class Rules for GCT vs TSV Files"
    - **GCT files** must always be imported with a `"dataClass": "Bulk transcriptomics"`.
    
    - **TSV files** are more flexible. You are not restricted to a single data class and can use any available one (e.g., *Proteomics*, *Metabolomics*, etc.) depending on the content. TSV imports support additional parameters such as `numberOfFeatureAttributes` and `measurementSeparator`, allowing you to define how features and measurements are organized within the file.

!!! note "Available Parameters"
    - **dataLink** - link to a file that contains the data.
    - **dataClass** - Specify a data class that suits the data set you are importing. You can use [Data Class](../import-data-in-odm/#data-type-data-class) list as a reference.
    - **metadataLink** - (optional) link to a file that contains metadata (.tsv)
    - **templateId** - (optional) accession of the template
    - **previousVersion** - (optional) accession of the previous version of the file. Used to update the existing version of the file.
    - **numberOfFeatureAttributes** - This field indicates how many columns in your file are related to the measured features (for example, Gene Names, Protein Names, Description, Metabolite Names, M/Z ratio, Retention Time, etc.). Please provide the correct number. Automatic recognition of this field will be added in future updates.
    - **measurementSeparator** - This parameter distinguishes the sample, library, or preparation name from various measurement types in your file's column headers (if applicable). For each sample, you might have different measurements like gene expression level, quality flag, sequencing depth, or p-value. This separator is crucial when your file contains columns for multiple such measurements. Supported separators include ., ,, :, ;, _, -, /, \, |, and multi-character separators are also allowed. Leave it blank if not applicable.


If successful, you will get the response that contain the **jobExecId** that we will use to get the **groupAccession** using `GET /api/v1/jobs/{jobExecId}/output` endpoint.

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF1283537"
  }
}
```

We can use the aquired **groupAccession** to get the expression data using `GET as-curator/omics/expression/data` endpoint:

```default
curl -X 'GET' \
  'https://<HOST>/api/v1/as-curator/omics/expression/data?exFilter=genestack%3Aaccession%20%3D%20GSF1283537' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```
As response you will get all the information, including the metadata, for the expression file we have succesfully imported.

```json
{
  "data": [
    {
      "itemId": "856314-ENSG00000077044",
      "itemOrigin": {
        "runSourceId": "HG00119",
        "runId": "856314",
        "groupId": "GSF1283537"
      },
      "metadata": {
        "Experimental Platform": null,
        "Features (numeric)": null,
        "Data Processing Method": null,
        "Genome Version": "GRCh37.68",
        "Scale": null,
        "Normalization Method": "RPKM",
        "Values (numeric)": null,
        "Data Class": "Bulk transcriptomics",
        "Pipeline ID": null,
        "Data Species": null,
        "Import Source URL": null,
        "Features (string)": null,
        "Data Files / Processed": null,
        "Data Files / Raw": null
      },
      "feature": {
        "feature": "ENSG00000077044"
      },
      "value": {
        "value": 14.7418793729
      },
      "relationships": null
    },

    Shortened for readability — 7 more items are not shown.
}
```

#### Linking to Samples/Libraries/Preparations

In this example, we link an expression group to a sample group using `POST /api/v1/as-curator/integration/link/{sourceType}/group/{sourceId}/to/{targetType}/group/{targetId}`and we will link another expression group to a library group using `POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/library/group/{targetId}`.

Alternatively, you can link to a preparations group using this endpoint:
- `POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/preparation/group/{targetId}`

!!! note "Linking library\preparation"
    When signal data is linked to **Libraries** or **Preparations**, the system uses a default attribute automatically:

    - For **Libraries**, the default linking attribute is `Library ID`
    - For **Preparations**, the default linking attribute is `Preparation ID`

There are two supported approaches for linking entities in the system:

##### Group-to-group linking

Use this approach when you want to link one group of objects (e.g., samples, libraries, or data entities) to another group. 

The call below links an expresison group to a sample group using the following endpoint:
`POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/sample/group/{targetId}`

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/as-curator/integration/link/expression/group/GSF1283537/to/sample/group/GSF1283530' \
  -H 'accept: */*' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -d ''
```

The call below links an expression group to a library group using the following endpoint:
`POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/library/group/{targetId}`

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/as-curator/integration/link/expression/group/GSF1284946/to/library/group/GSF1284497' \
  -H 'accept: */*' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -d ''
```


##### Object-to-object linking

Use this approach to link individual objects directly — for example, linking a specific data object to a specific sample.

The call below links a single source object to a single target object using the following endpoint:
`POST /api/v1/as-curator/integration/link/{sourceType}/{sourceId}/to/{targetType}/{targetId}`

```default
curl -X 'POST' \
  ' 'https://odm.demo.genestack.com/api/v1/as-curator/integration/link/expression/GSF282812/to/sample/HG00119' \
  -H 'accept: */*' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -d ''

```
Expression data is now succesfuly linked and visible in the GUI.
![api-expression-data-linked.png](../../doc-odm-user-guide/doc-odm-user-guide/images/api-expression-data-linked.png)

### Variant data 

- [Test_variant.vcf](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_variant.vcf), a [VCF](https://samtools.github.io/hts-specs/VCFv4.2.pdf) file of variant data from multiple sequencing runs

|   #CHROM |       POS | ID          | REF   | ALT   |   QUAL | FILTER   | INFO    | FORMAT   | HG00119   | HG00121   | HG00183   | HG00176   |
|----------|-----------|-------------|-------|-------|--------|----------|---------|----------|-----------|-----------|-----------|-----------|
|        2 | 233364596 | rs838705    | G     | A     |    100 | PASS     | AF=0.64 | GT       | 0|0       | 0|1       | 1|0       | 1|1       |
|        2 | 233385915 | rs201966773 | T     | TTC   |    987 | PASS     | AF=0.86 | GT       | 0|0       | 0|1       | 1|1       | 1|1       |

- [Test_variant.vcf.tsv](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_variant.vcf.tsv), a tab-separated file that describes the variant data

| Experimental Platform  |
|------------------------|
| IonTorrent Proton      |

#### Import process

Let's repeat the previous step, this time for variant data, ensuring that both expression and variant data are linked to the samples, reinforcing the data model hierarchy where samples are linked to a study, and data types (expression and variant) are linked to samples.

To import the variant data we will use `POST /api/v1/jobs/import/variant` endpoint:

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/variant?allow_dups=true' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_variant.vcf.tsv",
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_variant.vcf"
}'
```

As with the previous job endpoints, the response will include a *jobExecId*, which can be passed to the *job/output* endpoint to retrieve the variant group accession "GSF1283539".

Which we can use to query the data using the `GET /api/v1/as-curator/omics/variant/data` endpoint:

```default
curl -X 'GET' \
  'https://<HOST>/api/v1/as-curator/omics/variant/data?vxFilter=genestack%3Aaccession%20%3D%20GSF1283539' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```
Response will contain the variant data that we imported:

```json
{
  "data": [
    {
      "itemId": "2-233364596-G-A-856318",
      "itemOrigin": {
        "runSourceId": "HG00119",
        "runId": "856318",
        "groupId": "GSF1283539"
      },
      "metadata": {
        "Data Class": "Gene variant (VCF)",
        "Experimental Platform": "IonTorrent Proton",
        "Pipeline ID": null,
        "Data Processing Method": null,
        "Genome Version": null,
        "Processed Data Files": null,
        "Import Source URL": null,
        "Scale": null,
        "Raw Data Files": null,
        "Name": null
      }
      ...
  "resultsExhausted": true,
  "log": [
    "There are no restrictions related with library/preparation/sample/study query"
  ],
  "cursor": "2-233385915-T-TC-856321"
}
```

#### Linking to Samples

To link the variant group (GSF1283539) with the sample group (GSF1283530) we will use `POST /api/v1/as-curator/integration/link/variant/group/{sourceId}/to/sample/group/{targetId}` endpoint.

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/as-curator/integration/link/variant/group/GSF1283539/to/sample/group/GSF1283530' \
  -H 'accept: */*' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -d ''
```

Variant data is now succesfuly linked and visible in the GUI.
![variant_added.png](../../doc-odm-user-guide/doc-odm-user-guide/images/variant_added.png)

### Flow Cytometry Data

- [Test_FACS_Signals.facs](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_FACS_Signals.facs), a tab-separated file that contains signal readouts from FACS experiments per cell population and sample.

| Sample   | CellPopulation                               | ReadoutType | Color/Marker | Value   |
|----------|----------------------------------------------|-------------|--------------|---------|
| HG00119  | Total events                                 | Counts      |              | 189031  |
| HG00119  | Total events/Lymphocytes                     | Counts      |              | 182557  |
| HG00119  | Total events/Lymphocytes                     | Percentage  |              | 96.6    |
| HG00119  | Total events/Lymphocytes/Single Cells        | Counts      |              | 177879  |
| HG00119  | Total events/Lymphocytes/Single Cells        | Percentage  |              | 97.4    |

- [Test_FACS_Signals.facs.csv](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_FACS_Signals.facs.csv), a tab-separated file that describes the FACS data.

| Experimental Platform  |
|------------------------|
| FACS                   |


#### Import Process

To import the Flow Cytometry data we will use `POST /api/v1/jobs/import/flow-cytometry` endpoint.

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/flow-cytometry?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_FACS_Signals.facs"
}'
```

The response will include a *jobExecId*, which can be passed to the *job/output* endpoint to retrieve the Flow Cytometry group accession "GSF1284512".

Which we can use to query the data using the `GET /api/v1/as-user/flow-cytometries` endpoint:

```default
curl -X 'GET' \
  'https://<HOST>/api/v1/as-user/flow-cytometries?query=genestack%3Aaccession%20%3D%20GSF1284512' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

Response will contain the Flow Cytometry data we have imported:
```json
{
  "data": [
    {
      "itemId": "856561-1",
      "itemOrigin": {
        "runSourceId": "HG00119",
        "runId": "856561",
        "groupId": "GSF1284512"
      },
      "metadata": {
        "Data Class": "Flow Cytometry (FACS)",
        "Experimental Platform": null,
        "Pipeline ID": null,
        "Data Processing Method": null,
        "Processed Data Files": null,
        "Import Source URL": null,
        "Scale": null,
        "Raw Data Files": null,
        "Name": null
      },
      "feature": {
        "readoutType": "Counts",
        "cellPopulation": "Total events",
        "marker": ""
      },
      "value": {
        "value": 189031
      }
    },
```

#### Linking to Samples

To link the Flow Cytometry group (GSF1284512) with the sample group (GSF1283530) we will use `POST /api/v1/as-curator/integration/link/variant/group/{sourceId}/to/sample/group/{targetId}` endpoint.

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/as-curator/integration/link/flow-cytometry/group/GSF1284512/to/sample/group/GSF1284464' \
  -H 'accept: */*' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -d ''
```

Flow Cytometry data is now succesfuly linked and visible in the GUI.
![facs_added.png](../../doc-odm-user-guide/doc-odm-user-guide/images/facs_added.png)

### Attached Files

- [test_file_metadata.pdf](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/test_file_metadata.pdf), a PDF file containing a test table.

| File Name         | Sample ID | File Type | Checksum  | Description                            |
|-------------------|-----------|-----------|-----------|----------------------------------------|
| file_001.bam      | SMPL001   | BAM       | abc12345  | BAM file for whole genome sequencing   |
| file_002.vcf      | SMPL002   | VCF       | def67890  | VCF file with called variants          |
| file_003.fastq.gz | SMPL003   | FASTQ     | ghe98765  | Raw sequencing reads                   |

#### Import process

To import and link attached file to a study we will use `POST /api/v1/jobs/import/file` endpoint.

The example call contains a link to a file, the accession of the study the file will be linked to, and a Data Class for the imported file. You can use any available Data Class for the Attached file.

!!! note "Mandatory fields"
    Please note that `dataLink`, `studyAccession` and `dataClass` are mandatory fields and cannot be skipped.
     


```default
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/file' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/test_file_metadata.pdf",
  "studyAccession": "GSF1284490",
  "dataClass": "Document"
}'
```

Attached file is now succesfuly linked and visible in the GUI.
![attached-file.png](../../doc-odm-user-guide/doc-odm-user-guide/images/attached-file.png)

### Check that you can query the relationships between objects

Once you've created and linked the study, sample, library, preparations and expression objects you can do integration-aware queries via both the User Interface and APIs.

In the User Interface, you should be able to find your imported study using the study, sample, library, preparations and signal filters.

To do this via APIs, you can use the integration/omics endpoint to filter across studies, samples, libraries, preparations and signals, and retrieve a specific object type. For example, to get metadata about the samples associated with library LIB1:

```default
curl -X 'GET' \
  'https://<HOST>/api/v1/as-curator/integration/link/samples/by/libraries?filter=%22Library%20ID%22%3D%20LIB1' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

Which will return:

```json
{
  "meta": {
    "pagination": {
      "count": 2,
      "total": 2,
      "offset": 0,
      "limit": 2000
    }
  },
  "data": [
    {
      "genestack:accession": "GSF1283543",
      "Sample Source ID": "SRR6441188",
      "Sample Name": null,
      "Ancestry": null,
      "Age": null,
      "Tissue Type": null,
      "Condition": null,
      "Sex": "F",
      "Genotyping Method": null,
      "Collection Date": null,
      "Sample Type": null,
      "Age Unit": null,
      "Genomic DNA Yield": null,
      "Smoking Status": null,
      "Sample Source": "1000 Genomes Project",
      "Population": "British",
      "groupId": "GSF1283541"
    },
    {
      "genestack:accession": "GSF1283542",
      "Sample Source ID": "SRR6441195",
      "Sample Name": null,
      "Ancestry": null,
      "Age": null,
      "Tissue Type": null,
      "Condition": null,
      "Sex": "M",
      "Genotyping Method": null,
      "Collection Date": null,
      "Sample Type": null,
      "Age Unit": null,
      "Genomic DNA Yield": null,
      "Smoking Status": null,
      "Sample Source": "1000 Genomes Project",
      "Population": "British",
      "groupId": "GSF1283541"
    }
  ]
}
```

To get the preparation metadata objects which are linked to sample metadata we can use `GET /api/v1/as-curator/integration/link/preparations/by/samples` endpoint.


```default
curl -X 'GET' \
  'https://<HOST>/api/v1/as-curator/integration/link/preparations/by/samples?filter=%22Sample%20Source%20ID%22%20%3D%20HG00119' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

Example response:

```json
{
  "meta": {
    "pagination": {
      "count": 1,
      "total": 1,
      "offset": 0,
      "limit": 2000
    }
  },
  "data": [
    {
      "genestack:accession": "GSF1284503",
      "Preparation ID": "PREP1",
      "Sample Source ID": [
        "HG00119",
        "HG00121"
      ],
      "Kit Reagent": null,
      "Incubation Time": null,
      "Date Performed": null,
      "Method Protocol": null,
      "Preparation Step": null,
      "Volume Concentration": null,
      "Volume Unit": null,
      "groupId": "GSF1284502"
    }
  ]
}
```
