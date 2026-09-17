---
diataxis: how-to
tab: odm-api
---

# How to import expression data

Expression data is where the biology lives: the measurements you have gathered against the samples, libraries, and preparations already described in ODM. Bringing it in, and linking it back to those entities, is what turns a study's metadata into a dataset you can actually explore. This guide takes you from an expression file (GCT or TSV) to an imported expression group, then wires it to the samples, libraries, preparations, or cell metadata it belongs to.

For an overview of how the import steps fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorisation, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token and Curator group membership.
- An expression data file in GCT or TSV format. For format requirements, see the supported data formats documentation.
- Sample, library, preparation, or cell metadata already imported (the entity you intend to link expression data to).

## Send the import request

Point ODM at your file with `POST /api/v1/jobs/import/expression`. The request body carries a small set of fields, two of them always required and two that come into play only for certain files:

- `dataLink` (required): URL of the expression data file (GCT or TSV)
- `dataClass` (required): Data class (e.g., "Bulk transcriptomics", "Proteomics", "Single-cell transcriptomics")
- `metadataLink` (optional): URL of an optional metadata TSV file
- `templateId` (optional): Accession of the template to apply
- `previousVersion` (optional): Accession of the previous file version (for version updates)
- `numberOfFeatureAttributes` (conditional): Number of feature columns; mandatory for TSV files with multiple feature columns
- `measurementSeparator` (conditional): Separator between sample/library/preparation name and measurement type in column headers

The `dataClass` you choose depends on the file format. GCT files must always use `"dataClass": "Bulk transcriptomics"`. TSV files are more flexible and support any available data class, such as "Proteomics" or "Metabolomics".

### Importing a GCT file

For a GCT file, the request is straightforward: the data link, an optional metadata link, and the fixed `"Bulk transcriptomics"` data class.

```bash
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/expression?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "metadataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_expression.gct.tsv",
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_expression.gct",
  "dataClass": "Bulk transcriptomics"
}'
```

### Importing a TSV file with multiple feature attributes

A TSV file with several feature columns needs a little more description. Set `numberOfFeatureAttributes` to the number of feature columns, choose the data class that matches your data, and use `measurementSeparator` to tell ODM how column headers split the sample, library, or preparation name from the measurement type.

```bash
curl -X 'POST' \
  'https://<HOST>/api/v1/jobs/import/expression?allow_dups=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "dataLink": "https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_generic_expression.tsv",
  "numberOfFeatureAttributes": 4,
  "dataClass": "Proteomics",
  "measurementSeparator": "."
}'
```

## Track the job and get your accession

A successful import returns a `jobExecId`, since the work runs as a background job rather than handing you a result straight away. Once the job completes, query `GET /api/v1/jobs/{jobExecId}/output` to retrieve the expression group accession:

```json
{
  "status": "COMPLETED",
  "result": {
    "groupAccession": "GSF1283537"
  }
}
```

To confirm the data landed as expected, query it back with `GET /api/v1/as-curator/omics/expression/data?exFilter=genestack:accession = GSF1283537`. See [Search imported data](../../explore/search-imported-data.md) for query syntax details.

## Link the expression data

An imported expression group is not much use until it points at the entities it measures. Link it to the sample, library, preparation, or cell metadata group it belongs with. For the endpoints and the full linking workflow, including group-to-group versus object-to-object linking, see [Link entities after import](link-entities-after-import.md).

Prefer to upload a file directly instead of pointing ODM at an external URL? Use `POST /api/v1/jobs/import/expression/multipart`, described in the [Multipart uploads reference](multipart-uploads-reference.md).
