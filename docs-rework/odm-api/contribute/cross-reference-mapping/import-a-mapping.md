---
diataxis: how-to
tab: odm-api
---

# How to import a cross-reference mapping

This guide explains how to import a cross-reference mapping file (TXNAME → GENEID) and link it to an expression data file in ODM.

## Prerequisites

- An API token. See [Authentication and tokens](../../getting-started/authentication-and-tokens.md).
- Curator group membership, only Curators can upload mapping files and create links.
- A mapping TSV file hosted at an HTTPS location accessible to ODM.
- An expression data file already imported in ODM (to link the mapping to).

For an overview of the mapping file format, see [About cross-reference mapping](about-cross-reference-mapping.md).

## Step 1: Upload the mapping file

Submit a `POST` request to `/reference-data/xrefsets`. The request body supplies the URL of your mapping file, an optional data source label, optional metadata key/value pairs, and the mapping type:

```json
{
  "dataLink": "http://example-url.com/my-mapping.tsv",
  "dataSource": "arvados",
  "metadata": {
    "additionalProp1": "string",
    "additionalProp2": "string",
    "additionalProp3": "string"
  },
  "xrefSetType": "gene-transcript"
}
```

The response contains the accession of the newly created mapping object (for example, `GSF123456`). Record this accession. You need it for the linking step.

## Step 2: Link the mapping file to expression data

Submit a `POST` request to the `/links` endpoint in `integrationCurator`. Supply the accession of the mapping file and the accession of the expression group, with type labels identifying each:

```json
[
  {
    "firstId": "GSF123456",
    "firstType": "geneTranscriptMapping",
    "secondId": "GSF098765",
    "secondType": "expressionGroup"
  }
]
```

Expression data can be linked to a previously uploaded mapping file even if that mapping is already linked to a different expression data object.

## Next steps

- [Query mappings](query-mappings.md), find genes for transcripts or retrieve the mapping for genes in a study.
- [Update or remove mappings](update-or-remove-mappings.md), replace or delete a mapping.
