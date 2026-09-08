---
diataxis: how-to
tab: odm-api
---

# How to import flow cytometry data

Flow cytometry (FACS) data comes into ODM as its own entity, and like the other omics data types it only becomes useful once it is attached to the samples it was measured from. This guide takes you from a `.facs` file to a flow cytometry group in ODM, and then links that group to your samples so the measurements sit alongside the rest of a sample's story.

For a wider view of how the pieces fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorisation, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token and Curator group membership.
- A FACS data file (`.facs` format), optionally accompanied by a metadata TSV file. Both must be hosted at HTTP/HTTPS URLs, S3 URIs, or NFS paths. For format requirements, see the supported data formats documentation.
- Sample metadata already imported.

## Send the import request

Point ODM at your file with `POST /api/v1/jobs/import/flow-cytometry`. The one field the request needs is `dataLink`, the location of your `.facs` file:

```json
{
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_FACS_Signals.facs"
}
```

If you have a separate metadata TSV, add an optional `metadataLink` field pointing to it, and if you want the group to use a specific template, add `templateId` with that template's accession.

Putting it together, the call looks like this:

```bash
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/flow-cytometry?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_FACS_Signals.facs"
}'
```

## Track the job and verify the result

The import runs as a background job, so a successful request hands you a `jobExecId` rather than the data itself. Once the job completes, query `GET /api/v1/jobs/{jobExecId}/output` to retrieve the flow cytometry group accession (for example, `GSF1284512`).

To confirm the data landed as expected, query the flow cytometry group directly:

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/as-user/flow-cytometries?query=genestack%3Aaccession%20%3D%20GSF1284512' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

For query syntax and response format details, see [Search imported data](../../explore/search-imported-data.md).

## Linking to samples

Imported data stands on its own until you connect it, so the last step is to attach the flow cytometry group to the samples it belongs with. For the endpoint and the full linking workflow, see [Link entities after import](link-entities-after-import.md).

Prefer to upload a file directly instead of pointing ODM at a URL? Use the multipart upload endpoint described in the [Multipart uploads reference](multipart-uploads-reference.md).
