---
diataxis: how-to
tab: odm-api
---

# How to import attached files

Not everything you want to keep with a study belongs in its indexed, searchable metadata. Documents, reports, and supporting data files can travel with a study as attached files, linked to it so they stay together. This guide takes you from a file at a URL to an attachment sitting on your study.

Worth knowing up front: the contents of attached files are not indexed or made searchable. You can query them only by their metadata. For an explanation of indexed versus attached files, see [About querying data](../../explore/about-querying-data.md).

For a wider view of how the pieces fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorisation, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token and Curator group membership.
- An S3 bucket configured for ODM. An S3 bucket is mandatory for the attached files functionality in ODM.
- The file to attach, accessible at an HTTP/HTTPS URL, S3 URI, or as a local file for multipart upload.
- A study to attach the file to (you need the study's accession number).

## Send the import request

Point ODM at your file with `POST /api/v1/jobs/import/file`. Three fields are required, and two more are optional:

- `dataLink` (required): URL of the file to attach.
- `studyAccession` (required): accession of the target study.
- `dataClass` (required): data class for the file (for example, "Document" or "Bulk transcriptomics").
- `metadataLink` (optional): URL of an optional metadata TSV file.
- `source` (optional): file source type, one of `S3`, `HTTP`, or `LOCAL`.

A minimal call looks like this:

```bash
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

## See what the request creates

ODM creates the attached file as a file object and links it to the study you named automatically. Attached files need no separate linking call: the import handles both steps at once.

## Querying and downloading attached files

Once a file is attached, you have a few ways to reach it. To list all attached files, use `GET /api/v1/as-user/files`. To narrow that to the files attached to a specific study, use `GET /api/v1/as-user/integration/link/files/by/study/{id}`. And to pull a file back down, use `GET /api/v1/as-user/files/{id}/download`. For full details, see [Search attached files](../../explore/search-attached-files.md).

## Multipart upload alternative

If your file does not live at an external URL and you would rather upload it directly, use `POST /api/v1/jobs/import/file/multipart` instead. See the [Multipart uploads reference](multipart-uploads-reference.md) for how it works.

## Next steps

With your file attached, step back to [About the import workflow](about-the-import-workflow.md) to see where this fits among the other imports and what to bring in next.
