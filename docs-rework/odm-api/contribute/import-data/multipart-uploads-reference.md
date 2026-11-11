---
diataxis: reference
tab: odm-api
---

# Multipart uploads reference

The ODM import API includes multipart form-data endpoints for all common import workflows. These endpoints accept the import file directly in the HTTP request body, eliminating the need to host the file at an external URL before importing.

## When to use multipart endpoints

Use multipart endpoints when:

- The file is available locally and you want to avoid uploading it to external storage first.
- You want a single-request import flow.
- Your automation script generates files at runtime and needs to submit them immediately.
- You are building an interactive tool where users select files to upload.

## Supported multipart endpoints

| Endpoint | File format | Entity type |
| --- | --- | --- |
| `POST /api/v1/jobs/import/study/multipart` | TSV | Study metadata |
| `POST /api/v1/jobs/import/samples/multipart` | TSV | Sample metadata |
| `POST /api/v1/jobs/import/libraries/multipart` | TSV | Library metadata |
| `POST /api/v1/jobs/import/preparations/multipart` | TSV | Preparation metadata |
| `POST /api/v1/jobs/import/cells/multipart` | TSV | Cell metadata |
| `POST /api/v1/jobs/import/expression/multipart` | TSV or GCT | Tabular expression data |
| `POST /api/v1/jobs/import/variant/multipart` | VCF or TSV | Variant data |
| `POST /api/v1/jobs/import/flow-cytometry/multipart` | FACS or TSV | Flow cytometry data |
| `POST /api/v1/jobs/import/file/multipart` | Any supported format | Attached file |

## How multipart endpoints work

Each endpoint creates and processes the same type of import job as its non-multipart counterpart. The only difference is how the source file is provided: multipart endpoints accept the file via the `file` parameter in the request body, while non-multipart endpoints require a `dataLink` URL.

> **Important:** the `file` parameter must always be placed last in the list of request parameters.

The study endpoint is the one multipart endpoint that takes no study accession. The others need the accession of an existing study (`studyId`, or `studyAccession` for attached files), and ODM stores the uploaded file with that study. The study import creates the study, so when you import a study and its data by direct upload, run it first: its job output gives the new study's accession, which you then pass to the other multipart imports. Passing `studyId` does not link the imported group to the study; that is still a separate step, described in [Link entities after import](link-entities-after-import.md).

## Data management

Files uploaded via multipart endpoints are copied into ODM's internal S3 bucket. The file is maintained by ODM from that point; the original can be deleted from local storage. Files uploaded this way are marked with the `File copy stored` technical metadata field. For the study import, the marker is on the new study itself, and deleting the study deletes the uploaded file.

## Relationship to transformations

Multipart upload endpoints are also used internally by the Attachment Transformation functionality in ODM. See the [Transformations](../transformations/about-processors-controller.md) section for context on how transformations use these endpoints.
