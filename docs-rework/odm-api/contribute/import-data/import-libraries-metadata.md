---
diataxis: how-to
tab: odm-api
---

# How to import libraries metadata

Libraries build on the samples you have already brought into ODM. Each library links back to a sample, so importing library metadata is the step that attaches your libraries to the material they were prepared from. This guide takes you from a library metadata TSV file to a library group with its own accession, ready to be connected to your samples.

For a wider view of how the pieces fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorisation, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token and Curator group membership.
- A library metadata TSV file hosted at an HTTP/HTTPS URL, S3 URI, or NFS path. The `Sample Source ID` column is mandatory. It must contain the identifiers used to link each library to its corresponding sample.
- Sample metadata already imported. See [Import sample metadata](import-sample-metadata.md).

## Send the import request

Point ODM at your file with `POST /api/v1/jobs/import/libraries`. The request body carries a single field, `metadataLink`, the location of your TSV:

```json
{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_libraries.tsv"
}
```

One optional query parameter shapes the import: `allow_dups` (default `false`) controls whether duplicate Library IDs are accepted. Here is the full call, with `allow_dups` set to its default:

```bash
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/libraries?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_libraries.tsv"
}'
```

## Track the job and get your accession

Import runs as a background job, so a successful call does not hand you the library group straight away. Instead it returns a `jobExecId`. Once the import completes, query `GET /api/v1/jobs/{jobExecId}/output` to retrieve the library group accession:

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF1283547"
  }
}
```

Hold on to that accession. You will need it when you link the library group to your samples.

## Next steps

With your library group in place, connect it to the sample group it belongs to. See [Link entities after import](link-entities-after-import.md).

Prefer to upload a file directly instead of pointing ODM at a URL? Use the multipart upload endpoint described in the [Multipart uploads reference](multipart-uploads-reference.md).
