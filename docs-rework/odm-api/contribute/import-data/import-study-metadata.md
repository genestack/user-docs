---
diataxis: how-to
tab: odm-api
---

# How to import study metadata

Importing a study is the first move in getting your data into ODM. The study is the object everything else hangs off: samples, libraries, preparations, and omics data all link back to it, so this is the step you run before any other import. This guide takes you from a metadata TSV file to a study with its own accession, ready to receive that data.

For a wider view of how the pieces fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorisation, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token and Curator group membership.
- A study metadata TSV file hosted where ODM can reach it: an HTTP/HTTPS URL, an S3 URI, or an NFS path. For the file format itself, see the TSV format specification in the supported data formats documentation.

## Send the import request

Point ODM at your file with `POST /api/v1/jobs/import/study`. The only field the request needs is `metadataLink`, the location of your TSV:

```bash
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/study' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv"
}'
```

If you want the study to use a specific template, add an optional `templateId` field with the template's accession, which you can copy from the Template Editor. Leave it out and ODM applies the instance default template.

## Track the job and get your accession

Import runs as a background job, so the response does not hand you a study straight away. Instead it returns a `jobExecId` that you use to follow the job's progress:

```json
{
  "jobExecId": 2115,
  "startedBy": "your_name@genestack.com",
  "jobName": "IMPORT_STUDY_TSV",
  "status": "STARTING",
  "createTime": "2025-04-16 07:42:38"
}
```

Poll `GET /api/v1/jobs/{jobExecId}/info` to watch the status move through `STARTING`, `RUNNING`, and on to `COMPLETED` or `FAILED`. Once it completes, `GET /api/v1/jobs/{jobExecId}/output` returns the result, and with it the thing you actually came for, the study's accession:

```json
{
  "status": "COMPLETED",
  "result": {
    "accession": "GSF1147033"
  }
}
```

Hold on to that accession. It identifies your new study, and you will need it every time you link samples or data to it. For everything job monitoring can tell you, see [Manage import jobs](manage-import-jobs.md) and the [Job status codes reference](../../reference/job-status-codes-reference.md).

If you would rather see it with your own eyes, open the Study Browser: the new study is there, owned by your account.

## Next steps

With the study in place, bring in its data and wire it together. Start with [Import sample metadata](import-sample-metadata.md), then [Link entities after import](link-entities-after-import.md).

Prefer to upload a file directly instead of pointing ODM at a URL? Use the multipart upload endpoint described in the [Multipart uploads reference](multipart-uploads-reference.md).
