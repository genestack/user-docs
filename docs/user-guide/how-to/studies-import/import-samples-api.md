# Import samples and libraries (API)

**Role:** Contributor

> For a simpler GUI workflow, see [Import samples (interface)](import-samples-gui.md).

!!! abstract "About this guide"

    This article provides a detailed and technically in-depth guide to loading data into the platform via API.  
    It is intended for users with experience in working with RESTful APIs and programmatic workflows.

    If you're new to the platform or prefer a more user-friendly approach, we recommend the following alternatives:
    
    - [Importing your data via the GUI](import-samples-gui.md)
    - [Using a Python script to load your dataset](import-data-python.md)

On this page, you will find a brief explanation about data import via APIs, followed by a step-by-step example that
you can try. Please note that you need to be a member of the curator group in ODM to be able to import and edit data.

## What can I import?

You can import studies, samples, and any data in the tabular format:

- **Study**: the context of an experiment, such as the aim and statistical design.
- **Sample**: the biological attributes of a sample, such as tissue, disease, and treatment.
- **Libraries metadata**: TSV file describing sequencing libraries or other indexable data types. It includes information on library preparation, type (e.g., single-end or paired-end), protocol, barcodes, and platform.
- **Preparations metadata**: metadata describing how samples were prepared prior to data generation, applicable to proteomics, transcriptomics, and other data types.
- **Cell metadata**: all the information stored per cell (per barcode) that describes that cell and its context, separate from the actual molecular measurements (like the gene expression counts matrix which should be uploaded as expression within the ODM)
- **Data**: Includes transcriptomics, proteomics, gene variant, flow cytometry data, cell expression, and more. You can import the metadata (e.g. genome version, normalization
  method, and the locations of raw/processed data in your storage) together with the processed data (e.g. expression counts, genotypes).
- **Cross-reference mapping**: a list of transcript and gene ids and how they map to each other.
- **Attached Files**: Supplement your study by attaching related research materials like PDF, XLSX, DOCX, PPTX files, images, and more. Please note, contents of these attached files won't be indexed or made searchable.

Once imported, studies, samples, and data metadata will be queryable and editable from both the User Interface and APIs, whilst the signal data will only be queryable via APIs.


## Can I capture the relationships between studies, samples, and data?

Importing data has two stages. First, you import studies, samples, and data separately. Then, you link them together: samples are linked to a study, libraries and preparations are linked to samples, and omics data (e.g., transcriptomics, proteomics) are linked to samples or to libraries/preparations depending on the data type. Attached files are linked directly to a study. 

The **Sample Source ID** is used as the default linking key. You can choose another attribute from the template for linking data to samples. The data model and how it looks in the User Interface is shown below.

In addition to core data types, **Libraries**, **Preparations**, **Cell metadata** require special handling. These files must include the **Sample Source ID**, which is used to link them to the appropriate samples. 

The correct order of linking follows the system logic and available endpoints:

- **Samples** are linked to a **Study**
- **Libraries** and **Preparations** are linked to **Samples**
- **Cell metadata** is linked to **Samples** or **Libraries** or **Preparations**
- **Omics data** (e.g. transcriptomics, proteomics, cell expression) are linked to **Samples**, or to **Libraries/Preparations**, or to **Cell metadata** depending on the data type
- **Attached files** are linked directly to a **Study**


![image](../../assets/data_model.svg)

## Data Loading via APIs

To load the data via APIs each entity is created via a separate endpoint specific for
this data type. Then they are sequentially linked in the Integration layer.

## Where can I import the data from?

API allows loading files hosted at HTTP/HTTPS URLs, S3 URIs, and NFS paths for files stored in mounted ODM storage.

!!! danger "Limitation"
    1. S3 bucket is mandatory to upload and work with Attached files functionality in the ODM
    2. **Export**: if attachment's metadata was updated and got a new version, attached file cannot be exported itself from the ODM.
    **Workaround**: export is available from exporting whole Study. We are working on improvements for this functionality in the 1.61 release.

## Prerequisites

### Authorization Token

To authenticate when using the APIs, you need to provide a valid authorization token.

For instructions on how to generate a token, refer to the [Generate an API token](../users-access/generate-api-token.md) guide.


## Core Data Import Workflow

### Files Used in This Workflow
In this example, we will import tiny subset of data from the 1000 Genomes Project, consisting of the following files:


- [Test_1000g.study.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv), a tab-delimited file of the study attributes

| Study Source         | Study Description              | Target Disease   |
|----------------------|--------------------------------|------------------|
| 1000 Genomes Project | Subset of 1000 Genomes Project | Healthy          |


- [Test_samples.tsv](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_samples.tsv), a tab-delimited file of sample attributes.

| Sample Source        | Sample Source ID   | Sex   | Population   |
|----------------------|--------------------|-------|--------------|
| 1000 Genomes Project | HG00119            | M     | British      |
| 1001 Genomes Project | HG00121            | F     | British      |
| 1002 Genomes Project | HG00183            | M     | Finnish      |
| 1003 Genomes Project | HG00176            | F     | Finnish      |


- [Test_libraries.tsv](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_libraries.tsv), a tab-delimited file of library metadata.

| Library ID   | Sample Source ID      | Preparation Protocol   | Library Type      |
|--------------|-----------------------|------------------------|-------------------|
| LIB1         | HG00119`|`HG00121       | NGS                    | Spatial RNA-Seq-1 |
| LIB2         | HG00183               | NGS                    | RNA-Seq-1         |
| LIB3         | HG00176               | NGS                    | RNA-Seq-1         |


- [Test_preparations.tsv](https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_preparations.tsv), a tab-delimited file of preparation metadata.

 Sample Source ID      | Digestion              | Preparation ID    |
-----------------------|------------------------|-------------------|
 HG00119`|`HG00121       | Trypsin                | PREP1             |
 HG00183               | Trypsin                | PREP2             |
 HG00176               | Trypsin                | PREP3             |


### Import Study

There are specific endpoints to import specific data types, as listed in the [**Swagger API documentation**](/swagger/?urls.primaryName=job). 

![api-navigate-swagger.gif](../../doc-odm-user-guide/doc-odm-user-guide/gifs/api-navigate-swagger.gif)

For data import, you should go to the job section and choose the endpoint relevant for the specific data type. For studies, use the `POST /api/v1/jobs/import/study` method, and supply the file URL:

```default
{
  "metadataLink": "https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv"
}
```


![api-add-study.gif](../../doc-odm-user-guide/doc-odm-user-guide/gifs/api-add-study.gif)


!!! note "templateId"
    You can include an optional parameter **"templateId"** to specify which template should be associated with the loaded data. You will need to provide the accession of the desired template, which can be obtained from Template Editor. If the "templateId" parameter is not specified, the default template set for the instance will be used.

Example of the curl call:
```default
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/study' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv"
}'
```

If successful, you should see the **jobExecId** that can be used to monitor the status of the import task

```json
{
  "jobExecId": 2115,
  "startedBy": "your_namel@genestack.com",
  "jobName": "IMPORT_STUDY_TSV",
  "status": "STARTING",
  "createTime": "2025-04-16 07:42:38"
}
```
!!! note "jobExecId"
    The response returns a jobExecId, which can be used to monitor and fetch the status of the import. Learn more about [working with jobID](#working-with-the-jobexecid).


You can also confirm this visually, by going to the **Study Browser** and check that a new study has been created,
owned by you:

![image](../../doc-odm-user-guide/doc-odm-user-guide/images/empty_study.png)


### Import Samples

To import samples, you should use a different endpoint, `POST /api/v1/jobs/import/samples`:
![api-add-samples.gif](../../doc-odm-user-guide/doc-odm-user-guide/gifs/api-add-samples.gif)

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/samples?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_samples.tsv"
}'
```

Similar to the previous step, you should see the **jobExecId** in the response:

```json
{
  "jobExecId": 2117,
  "startedBy": "job@genestack.com",
  "jobName": "IMPORT_SAMPLES_TSV",
  "status": "STARTING",
  "createTime": "2025-04-16 13:47:17"
}
```
As soon as the import process will be completed, you will be able to get the sample **groupAccession** by querying the **jobExecId** in `GET /api/v1/jobs/{jobExecId}/output` endpoint:

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF1283530"
  }
}
```

However, you won't see the samples in the Study Browser yet, because no samples have been linked to the study.

### Import Libraries

The next step is to import a library metadata file . First we import the library file using a `POST /api/v1/jobs/import/libraries` endpoint:

!!! note "Mandatory attribute for libraries: Sample Source ID"
    In **libraries** files, the `Sample Source ID` column is mandatory. It must contain the identifiers used to link each library to its corresponding sample.


```default
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/libraries?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_libraries.tsv"
}'
```

This returns similarly to the samples import - [jobExecId](#working-with-the-jobexecid), using the `GET /api/v1/jobs/{jobExecId}/output` endpoint we will get the groupAccession. 

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF1283547"
  }
}
```

### Import Preparations

To import preparations, you will need to use `POST /api/v1/jobs/import/preparations` endpoint:

!!! note "Mandatory attribute for preparations: Sample Source ID"
    In **preparations** files, the `Sample Source ID` column is mandatory. It must contain the identifiers used to link each preparation to its corresponding sample.


```default
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/preparations?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_preparations.tsv"
}'
```

Similar to the previous step, you should see the **jobExecId** in the response:

```json
{
  "jobExecId": 2238,
  "startedBy": "job@genestack.com",
  "jobName": "IMPORT_PREPARATIONS_TSV",
  "status": "STARTING",
  "createTime": "2025-05-14 09:52:26"
}
```
As soon as the import process will be completed, you will be able to get the preparations **groupAccession** by querying the **jobExecId** in `GET /api/v1/jobs/{jobExecId}/output` endpoint:

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF1284256"
  }
}
```

### Import Cell metadata

For working with Cell metadata and Cell expression use the following example files:

- [Study_metadata](https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/study_metadata.tsv), a tab-delimited file of the study attributes
- [Samples_metadata](https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/samples.tsv), a tab-delimited file of sample attributes
- [Cell_metadata](https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/cells_2_samples_full_match.tsv), a tab-delimited file of cell attributes
- [Cell_expression](https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/expression_2_cells_linked_to_samples.tsv), a tab-delimited file of cell expression data

To import Cell metadata, you will need to use `POST /api/v1/jobs/import/cells` endpoint:

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/cells?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/cells_2_samples_full_match.tsv"
```

Similar to the previous step, you should see the **jobExecId** in the response:

```json
{
  "jobExecId": 24,
  "startedBy": "job@genestack.com",
  "jobName": "IMPORT_CELLS",
  "status": "COMPLETED",
  "createTime": "2026-02-05 11:35:36",
  "endTime": "2026-02-05 11:35:38"
}
```
As soon as the import process will be completed, you will be able to get the Cell metadata **groupAccession** by querying the **jobExecId** in `GET /api/v1/jobs/{jobExecId}/output` endpoint:

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF016786"
  }
}
```

### Multipart form-data upload endpoints

The Jobs import API includes `multipart/form-data` endpoints for common ODM import workflows. 
These endpoints allow uploading import files directly as part of the request, without providing 
a `dataLink` to an external file location.

This simplifies import workflows where the source file is already available locally. 
Instead of uploading a file to external storage first and then passing its URL to the API, you can 
submit the file directly to the corresponding import endpoint.

#### Supported endpoints

The following multipart endpoints are available:

* `POST /api/v1/jobs/import/samples/multipart`
  Uploads **Sample metadata** in **TSV** format.

* `POST /api/v1/jobs/import/libraries/multipart`
  Uploads **Library metadata** in **TSV** format.

* `POST /api/v1/jobs/import/preparations/multipart`
  Uploads **Preparation metadata** in **TSV** format.

* `POST /api/v1/jobs/import/cells/multipart`
  Uploads **Cell metadata** in **TSV** format.

* `POST /api/v1/jobs/import/expression/multipart`
  Uploads **tabular expression data** in **TSV** or **GCT** format.

* `POST /api/v1/jobs/import/variant/multipart`
  Uploads **variation data or metadata** in **VCF** or **TSV** format.

* `POST /api/v1/jobs/import/flow-cytometry/multipart`
  Uploads **flow cytometry data or metadata** in **FACS** or **TSV** format.

* `POST /api/v1/jobs/import/file/multipart`
  Uploads a **file attachment** through the Jobs import workflow.

#### How these endpoints work

Each endpoint is designed for a specific import type and accepts the uploaded file as multipart form data. 
The API then creates and processes the corresponding import job in the same way as the existing Jobs import flow.

The main difference from the non-multipart import endpoints is how the source file is provided:

* **Multipart endpoints** accept the file directly in the HTTP request body via `file` parameter. Please note that
    **the `file` parameter must always be placed last in the list of request parameters.**
* **Non-multipart endpoints** require a `dataLink` that points to the source file in external storage.

!!! tip "Data management"
    The files uploaded via multipart endpoints are copied into ODM internal S3 bucket. 
    The files are maintained by ODM and can be deleted from the original storage. 
    Additionally such files are marked with `File copy stored` technical metadata field.

#### When to use multipart endpoints

Use multipart upload endpoints when:

* you already has the file available locally
* you want to avoid the extra step of uploading the file to external storage
* you want a simpler, single-request import flow for supported import types

These endpoints are particularly useful for importing files dynamically at runtime. 
Interactive tools can submit files chosen by the user directly to the API, automation scripts can generate 
and upload supported files as part of a single automated workflow, and system integrations can collect data 
from external sources, convert it into a supported format, and submit it immediately. 
This approach eliminates the need for intermediate file hosting and simplifies direct file-based import flows.
Such flows are also supported 
within **[Attachment transformation functionality](transform-attachments.md)** in ODM.


### Linking entities

#### Samples to Study

You can link samples to study using the integration endpoint `POST /api/v1/as-curator/integration/link/sample/group/{sourceId}/to/study/{targetId}`, specifying the accessions of the study and the accession of the sample group. This will link all samples from the imported file to the study. The following call will link samples that we imported in the previous step (with accession GSF1283530) to the study
(with accession GSF1283528):

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/as-curator/integration/link/sample/group/GSF1283530/to/study/GSF1283528' \
  -H 'accept: */*' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -d ''
```

If successful, in the Study Browser you should see that the number of samples next
to your study has changed from '-' to '4':

![sample_added.gif](../../doc-odm-user-guide/doc-odm-user-guide/gifs/sample_added.gif)

Samples from other files can be loaded in the same way. They will be displayed in the Metadata Editor on a separate subtab.

!!! note "Data Import using Python script"
    If your goal is to perform a one-time import and create a single study, we recommend using our provided [API script](import-data-python.md) for simplicity and efficiency.

#### Libraries to Samples

You can link the **library group** to the **samples group** using the endpoint `POST /api/v1/as-curator/integration/link/library/group/{sourceId}/to/sample/group/{targetId}`, along with the **accession** returned when importing the samples.

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/as-curator/integration/link/library/group/GSF1283547/to/sample/group/GSF1283541' \
  -H 'accept: */*' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -d ''
```


If successful you will see a library tab appear in the Metadata Editor:

![image](../../doc-odm-user-guide/doc-odm-user-guide/images/library-added.png)

#### Preparations to Samples

You can link the **preparation group** to the **samples group** using the endpoint `POST /api/v1/as-curator/integration/link/preparation/group/{sourceId}/to/sample/group/{targetId}`, along with the **accession** returned when importing the samples.

```default
curl -X 'POST' \
  'https://<HOST>/api/v1/as-curator/integration/link/preparation/group/GSF1284256/to/sample/group/GSF1284456' \
  -H 'accept: */*' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -d ''
```
If successful you will see a preparation tab appear in the Metadata Editor:

![image](../../doc-odm-user-guide/doc-odm-user-guide/images/preparation-added.png)

#### Cell metadata to Samples/Libraries/Preparations

You can link the **Cell metadata group** to the **samples/libraries/preparation groups** using the endpoints:

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

If successful you will find the Cells via `GET /api/v1/as-curator/omics/cells` API endpoint when Study accession is provided for `studyQuery` parameter.

### Working with the jobExecId

The following endpoints allow you to manage and inspect jobs using the jobExecId, which is returned after initiating an asynchronous import task.

#### Monitoring job status

**GET /api/v1/jobs/{jobExecId}/info**

Retrieves the current status and metadata of a specific job execution.

- **Use case**: Use this to monitor the progress of an import job using its `jobExecId`.
- **Endpoint**: `GET /api/v1/jobs/{jobExecId}/info`

![api-get-job-info.gif](../../doc-odm-user-guide/doc-odm-user-guide/gifs/api-get-job-info.gif)

!!! note "Status codes"
    The job status can be one of the following:

    - **STARTING** – Import job is starting  
    - **RUNNING** – Import job is in progress  
    - **COMPLETED** – Import job was successful  
    - **FAILED** – Import job failed with an error

---

**GET /api/v1/jobs/{jobExecId}/output**

Retrieves the output of a completed job, including the accession of the generated study.

- **Use case**: Use this after a job has completed to get the final result and study accession.
- **Endpoint**: `GET /api/v1/jobs/{jobExecId}/output`

![api-get-job-output.gif](../../doc-odm-user-guide/doc-odm-user-guide/gifs/api-get-job-output.gif)

```json
{
  "status": "COMPLETED",
  "result": {
    "accession": "GSF1283528"
  }
}
```

---

**PUT /api/v1/jobs/{jobExecId}/restart**

Restarts a job that has failed or was stopped before completion.

- **Use case**: If a job failed due to a temporary issue, you can restart it using its `jobExecId`.
- **Endpoint**: `PUT /api/v1/jobs/{jobExecId}/restart`

---

**PUT /api/v1/jobs/{jobExecId}/stop**

Stops a job that is currently running.

- **Use case**: Use this when you need to cancel a long-running or stuck job.
- **Endpoint**: `PUT /api/v1/jobs/{jobExecId}/stop`

---

!!! note "Behavior by file type"
    The behavior of stop and restart actions depends on the type of file being processed:

    - **Metadata files** (studies, libraries, preparations, samples): Stop and restart are supported. The job resumes from where it left off.
    - **Signal files** (expression, flow cytometry, variant): These are processed very quickly, so stopping and restarting has limited practical use.
    - **Attachment files** (e.g., documents, images): These are handled as a single unit, so stop and restart are not applicable.

## What's next

Once you have imported a study and samples, proceed to [Import omics data (API)](import-omics-data-api.md) to import signal data such as expression, variant, and flow cytometry data.
