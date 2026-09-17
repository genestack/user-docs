---
diataxis: how-to
tab: odm-api
---

# How to import sample metadata

With your study in place, the next thing to bring in is its samples. Importing sample metadata registers your samples in ODM as a sample group, ready to be linked to the study they belong to. This guide takes you from a sample metadata TSV file to a sample group with its own accession, the value you carry forward into the linking step.

For a wider view of how the pieces fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorization, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token and Curator group membership.
- A sample metadata TSV file hosted at an HTTP/HTTPS URL, S3 URI, or NFS path. The file must include the required columns **Sample Source** and **Sample Source ID**. For the TSV format specification, see the supported data formats documentation.

## Send the import request

Point ODM at your file with `POST /api/v1/jobs/import/samples`. The one field the request needs is `metadataLink`, the location of your TSV:

```json
{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_samples.tsv"
}
```

If you want the samples to use a specific template, add an optional `templateId` field to specify which template to apply. Leave it out and ODM applies the instance default template.

Here is the complete call. Note the `allow_dups` query parameter, which defaults to `false` and controls whether duplicate Sample Source IDs are accepted:

```bash
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/samples?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_samples.tsv"
}'
```

## Track the job and get your accession

Import runs as a background job, so a successful call does not hand you the sample group straight away. Instead it returns a `jobExecId` that you use to follow the job's progress:

```json
{
  "jobExecId": 2117,
  "startedBy": "job@genestack.com",
  "jobName": "IMPORT_SAMPLES_TSV",
  "status": "STARTING",
  "createTime": "2025-04-16 13:47:17"
}
```

Once the import completes, query `GET /api/v1/jobs/{jobExecId}/output` to retrieve the sample group accession:

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF1283530"
  }
}
```

The `groupAccession` value is the accession of the newly created sample group. Hold on to it, because you need it for the linking step.

One thing to expect: the samples will not appear in the Study Browser until they are linked to a study.

## Next steps

Link the sample group to the study. See [Link entities after import](link-entities-after-import.md).

Prefer to upload a file directly instead of pointing ODM at a URL? Use the multipart upload endpoint described in the [Multipart uploads reference](multipart-uploads-reference.md).
