---
diataxis: how-to
tab: odm-api
---

# How to import variant data

Variant data is where your VCF calls join the samples they belong to inside ODM, so you can query the variants and the biology around them together. This guide takes you from a VCF file to a variant group that lives in your study and links back to its samples.

For a wider view of how the pieces fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorisation, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token and Curator group membership.
- A VCF file and optionally a metadata TSV file, both hosted at HTTP/HTTPS URLs, S3 URIs, or NFS paths. For the VCF format specification and ODM-specific requirements, see the supported data formats documentation on VCF.
- Sample metadata already imported.

## Send the import request

Point ODM at your files with `POST /api/v1/jobs/import/variant`. The request body carries two links: `dataLink` for the VCF file, and `metadataLink` for its metadata TSV:

```json
{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_variant.vcf.tsv",
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_variant.vcf"
}
```

One thing to know before you run it: for variant data the `allow_dups` parameter defaults to `true` (unlike other entity types). Putting it together, the call looks like this:

```bash
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

## Track the job and get your accession

A successful import returns a `jobExecId`. Once the job completes, query `GET /api/v1/jobs/{jobExecId}/output` to retrieve the variant group accession (for example, `GSF1283539`).

To confirm the data landed, query the variant group you just created:

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/as-curator/omics/variant/data?vxFilter=genestack%3Aaccession%20%3D%20GSF1283539' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

For variant query syntax including `vxQuery`, `variantFeature`, `variantInfo`, and `referenceGenomeId` parameters, see [Search imported data](../../explore/search-imported-data.md).

## Reference genome

If you plan to filter by gene name, keep in mind that the `variantFeature` query parameter needs a reference genome linked to the variant group. Refer to the API documentation for the reference genome upload endpoint.

## Linking to samples

To tie the variant group to its samples, link it to the sample group. For the endpoint and the full linking workflow, see [Link entities after import](link-entities-after-import.md).

Prefer to upload a file directly instead of pointing ODM at a URL? Use the multipart upload endpoint described in the [Multipart uploads reference](multipart-uploads-reference.md).
