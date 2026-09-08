---
diataxis: how-to
tab: odm-api
---

# How to import preparations metadata

Once your samples are in ODM, preparations are the next link in the chain. Each preparation ties back to a sample, so this step builds on the sample import you have already run and moves your data one step closer to being fully connected. This guide takes you from a preparation metadata TSV file to a preparation group with its own accession, ready to be linked to its samples.

For a wider view of how the pieces fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorisation, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token and Curator group membership.
- A preparation metadata TSV file hosted at an HTTP/HTTPS URL, S3 URI, or NFS path. The `Sample Source ID` column is mandatory. It must contain the identifiers used to link each preparation to its corresponding sample.
- Sample metadata already imported. See [Import sample metadata](import-sample-metadata.md).

## Send the import request

Point ODM at your file with `POST /api/v1/jobs/import/preparations`. The only field the request body needs is `metadataLink`, the location of your TSV:

```json
{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_preparations.tsv"
}
```

You can also tune how ODM handles repeated identifiers with the `allow_dups` query parameter (default: `false`), which controls whether duplicate Preparation IDs are accepted. Putting it together, the full call looks like this:

```bash
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/preparations?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_preparations.tsv"
}'
```

## Track the job and get your accession

Import runs as a background job, so the response does not hand you a preparation group straight away. Instead a successful call returns a `jobExecId` that you use to follow the job's progress:

```json
{
  "jobExecId": 2238,
  "startedBy": "job@genestack.com",
  "jobName": "IMPORT_PREPARATIONS_TSV",
  "status": "STARTING",
  "createTime": "2025-05-14 09:52:26"
}
```

Once the import completes, query `GET /api/v1/jobs/{jobExecId}/output` to retrieve the result, and with it the thing you actually came for, the preparation group accession:

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF1284256"
  }
}
```

## Next steps

With the preparation group in place, link it to the sample group. See [Link entities after import](link-entities-after-import.md).

Prefer to upload a file directly instead of pointing ODM at a URL? Use the multipart upload endpoint described in the [Multipart uploads reference](multipart-uploads-reference.md).
