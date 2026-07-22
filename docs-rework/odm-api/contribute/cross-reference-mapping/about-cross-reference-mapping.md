---
diataxis: explanation
tab: odm-api
---

# About cross-reference mapping

ODM allows you to import and link a cross-reference (xref) mapping file. The mapping enables you to look up genes for a given set of transcripts and vice versa. Mappings are associated with expression data files, though if needed you can query all mapping files across the organisation to return all mappings. All mapping file operations are carried out via the API.

## The mapping file format

An xref mapping file is a TSV file with two columns. The first row must contain the column headers `TXNAME` and `GENEID`. The first column contains transcript IDs, which must be unique. The file must be hosted at an HTTPS location accessible to ODM.

| TXNAME | GENEID |
|---|---|
| ENST00000438176.2 | ENSG00000231103.2 |
| ENST00000445563.2 | ENSG00000226662.2 |

## Metadata about the mapping

When importing a mapping file you can supply arbitrary key/value pairs in the request body, for example, `"organism": "Homo sapiens"`. This metadata is stored with the mapping object and can be inspected later via the API.

## API surface

The current API uses the `/xrefsets/*` endpoints found under the `reference-data` section in Swagger. Linking a mapping to an expression group uses the `/links` endpoint in `integrationCurator`.

- [Import a mapping](import-a-mapping.md), upload a mapping file and link it to expression data.
- [Query mappings](query-mappings.md), find genes for transcripts, retrieve mappings for a study, or check availability.
- [Update or remove mappings](update-or-remove-mappings.md), delete and replace a mapping or remove it entirely.

## Who can do what

- To upload mapping files and create or delete links: you must be a member of the Curator group.
- To query mappings: any user can do this. Mappings are shared across all members of an organisation.
- To delete a mapping file: only the original uploader of the mapping file can delete it.
