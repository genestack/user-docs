---
diataxis: explanation
tab: odm-api
---

# About the import workflow

This page explains how data import works in the ODM API and introduces the import-then-link pattern used across all entity types.

This section covers programmatic import via the REST API. If you prefer a GUI-based approach, see [Importing data](../../../contribute/import-data/index.md). For one-time imports using a script, consider the ODM SDK: [Upload a study](../../../api-libraries/odm-sdk/study/upload-a-study.md). All import operations via the API require Curator group membership.

## What you can import

The ODM API supports import of the following entity types:

- **Study**, the context of an experiment, including aim, statistical design, and descriptive metadata.
- **Sample metadata**, biological attributes of samples (tissue, disease, treatment, etc.).
- **Libraries metadata**, sequencing library information: preparation method, library type, protocol, barcodes, and platform.
- **Preparations metadata**, sample preparation details prior to data generation (applicable to proteomics, transcriptomics, and other data types).
- **Cell metadata**, per-barcode cell information, separate from the actual molecular measurements.
- **Tabular data**, expression, variant, flow cytometry, and other tabular data types, including both metadata and processed data values.
- **Attached files**, supplementary materials such as PDFs, spreadsheets, images, and archives. Note: the contents of attached files are not indexed or made searchable.

## The import-then-link workflow

Import is a two-stage process. First, each entity is imported via its own endpoint. Second, entities are linked together using the integration endpoints. Each entity import returns a `jobExecId` that you use to track the job and retrieve the entity's accession number, which you then supply in the linking step.

The required linking order is:

1. Samples → Study
2. Libraries and Preparations → Samples
3. Cell metadata → Samples, Libraries, or Preparations
4. Omics data → Samples, Libraries/Preparations, or Cell metadata (depending on data type)
5. Attached files → Study

For the linking step, see [Link entities after import](link-entities-after-import.md).

## The default linking key

The **Sample Source ID** attribute is used as the default key for linking data to samples. You can substitute any other template attribute as the linking key. For libraries, the default key is **Library ID**; for preparations, it is **Preparation ID**.

## Where you can import from

The API accepts files hosted at HTTP/HTTPS URLs, S3 URIs, and NFS paths for files stored in mounted ODM storage. For direct file upload without an external URL, use the multipart upload endpoints. See [Multipart uploads reference](multipart-uploads-reference.md).

An NFS path is a `file://` link, and it must lie under the mounted storage: `/local_data`, unless your administrator configured other directories. A `file://` link outside them, with a `..` segment, or through or to a symbolic link answers `400`.

An HTTP/HTTPS URL answers `400` when its host is `localhost`, or is or resolves to a loopback, link-local, any-local or multicast address, such as `127.0.0.1` or `169.254.169.254`.

## The asynchronous job model

Most import operations are asynchronous. The endpoint first checks that ODM can read every file the request links to. A link ODM cannot read answers `404` with hint `A0003` ("The system cannot open the file ..."), and no job is created. Otherwise, the endpoint responds immediately with a `jobExecId`. Use `GET /api/v1/jobs/{jobExecId}/info` to check the status (STARTING, RUNNING, COMPLETED, FAILED) and `GET /api/v1/jobs/{jobExecId}/output` to retrieve the result, typically the new entity's accession number. For full details, see [Manage import jobs](manage-import-jobs.md) and the [Job status codes reference](../../reference/job-status-codes-reference.md).
