---
diataxis: how-to
tab: odm-api
---

# How to import cell metadata

Cell metadata is how single-cell data takes its place in a study. Each row describes one cell and carries the key that ties it back to the samples, libraries, or preparations you have already imported, so this is the step that turns a standalone counts file into data ODM can navigate. This guide takes you from a cell metadata TSV file to a cell metadata group with its own accession, ready to link to its parent entity.

For an overview of how the import pieces fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorisation, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token and Curator group membership.
- A cell metadata TSV file. The required columns are `barcode` (must be unique within the group) and `batch` (used as the linking key to samples, libraries, or preparations).
- Sample, library, or preparation metadata already imported (the entity type you intend to link cell metadata to).

Cell metadata import accepts TSV files only.

## Send the import request

Point ODM at your file with `POST /api/v1/jobs/import/cells`. This endpoint differs from the study, sample, library, and preparation imports in one detail worth noting: it expects the file location in a `dataLink` field, not the `metadataLink` those imports use.

```json
{
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/cells_2_samples_full_match.tsv"
}
```

One query parameter shapes the import: `allow_dups` (default `false`) controls whether duplicate barcodes are accepted. Putting it together, the full call looks like this:

```bash
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/cells?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/User_guide_test_data/Single_cell_data/cells_2_samples_full_match.tsv"
}'
```

## Track the job and get your accession

Import runs as a background job, so the file is not ingested the instant you send the request. Once it completes, query `GET /api/v1/jobs/{jobExecId}/output` to retrieve the cell metadata group accession:

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF016786"
  }
}
```

Hold on to that accession: it identifies your cell metadata group when you link it to its parent entity. For the cell metadata attribute structure and validation rules, see the [Cell metadata reference](../../reference/cell-metadata-reference.md).

## Multipart upload alternative

Prefer to upload a file directly instead of pointing ODM at an external URL? Use `POST /api/v1/jobs/import/cells/multipart`. The [Multipart uploads reference](multipart-uploads-reference.md) covers it.

## Next steps: linking

With the group imported, connect it to its parent sample, library, or preparation group. Cell metadata links by matching the `batch` values in your file to the `Sample Source ID`, `Library ID`, or `Preparation ID` in the target group. For the endpoints and the full linking workflow, see [Link entities after import](link-entities-after-import.md).

## Cell expression

Cell expression data (the gene expression counts matrix) has its own path: it is imported via the expression import endpoint, not the cell metadata endpoint. After importing it, link the expression group to this cell metadata group. For the full expression import workflow, see [Import expression data](import-expression-data.md), and for the linking step, see [Link entities after import](link-entities-after-import.md). For cell expression data, TSV files archived in `.br` or `.lz4` format are recommended.
