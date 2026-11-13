---
diataxis: how-to
tab: odm-api
---

# How to find a template and read its fields

> **[BETA]** The template endpoints are in BETA and are subject to change. Backward compatibility is not guaranteed.

Study, sample, library, preparation and omics data imports take an optional `templateId`, the accession of the template ODM applies to the imported metadata. `GET /api/v1/templates` lists the templates with their accessions. `GET /api/v1/templates/{id}` returns one template with its fields, so you can check which fields your metadata TSV needs before you import it.

For a wider view of how the pieces fit together, see [About the import workflow](about-the-import-workflow.md), and for tokens and authorisation, see [Authentication and tokens](../../getting-started/authentication-and-tokens.md). For the full endpoint specification, the [`templates` definition in Swagger](/swagger/?urls.primaryName=templates) is the source of truth.

## Prerequisites

- An ODM account. Both endpoints are open to every ODM user, and Curator group membership is not needed. To run the curl examples, you also need a Genestack API token or an Identity Provider access token.

## List the templates

Call `GET /api/v1/templates`:

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/templates' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

The response is an array with one entry for each template you can read:

```json
[
  {
    "id": "GSF000123",
    "name": "Default template",
    "description": "Template applied to studies imported without one",
    "isDefault": true
  },
  {
    "id": "GSF000789",
    "name": "Oncology template",
    "isDefault": false
  }
]
```

- `id` is the template's accession. An import request takes this value as `templateId`.
- `name` is the template's name.
- `description` is the template description. It is absent when the template has none.
- `isDefault` is `true` for the organisation's default template. Import applies the default template when a request has no `templateId`.

## Read a template's fields

Pass the template's accession to `GET /api/v1/templates/{id}`:

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/templates/GSF000123' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

The response has the same `id`, `name`, `description` and `isDefault` as the list. It adds `fields`, the template's fields for every data type:

```json
{
  "id": "GSF000123",
  "name": "Default template",
  "description": "Template applied to studies imported without one",
  "isDefault": true,
  "fields": [
    {
      "name": "Sample Source ID",
      "dataType": "genestack:sampleObject",
      "metainfoType": "com.genestack.api.metainfo.StringValue",
      "isRequired": true,
      "isReadOnly": true,
      "description": "Unique sample identifier"
    },
    {
      "name": "Organism",
      "dataType": "genestack:sampleObject",
      "metainfoType": "com.genestack.api.metainfo.StringValue",
      "isRequired": true,
      "isReadOnly": false,
      "dictionaryAccession": "GSF000456",
      "dictionaryName": "NCBI Taxonomy"
    }
  ]
}
```

`fields` lists only the fields a metadata file supplies. The technical fields ODM fills itself are left out: `genestack:accession` for every data type, `Data Class` for expression, variant and flow cytometry groups, and `Features (string)`, `Features (numeric)` and `Values (numeric)` for expression groups (see [Mandatory technical fields](../../../contribute/templates/template-reference.md#mandatory-technical-fields)).

The endpoint returns HTTP status `404` when no template has that accession, or when you cannot read the template.

A field has the properties of the template upload format that the [Template reference](../../../contribute/templates/template-reference.md#template-json-file-structure) describes, plus `dictionaryAccession`, which that format lacks. To upload a template with `odm-update-template`, drop `dictionaryAccession` from each field, then save the `fields` array as a template JSON file (see [Create or update a template](../../../api-libraries/odm-sdk/templates/create-or-update-a-template.md)). When you cannot read a field's dictionary, `dictionaryName` is absent, so a template you save and upload again loses that field's dictionary.

Each field carries these properties:

| Property | Description |
| --- | --- |
| `name` | Name of the template key, unique within its data type |
| `dataType` | Data type the field applies to, by its internal name. See the values below. |
| `metainfoType` | Java class of the field's values: `com.genestack.api.metainfo.StringValue` (text), `com.genestack.api.metainfo.IntegerValue` (a whole number), `com.genestack.api.metainfo.DecimalValue` (a number), `com.genestack.api.metainfo.BooleanValue` (`true` or `false`), `com.genestack.api.metainfo.DateTimeValue` (a date, with or without a time) or `com.genestack.api.metainfo.ExternalLink` (a URL) |
| `isRequired` | `true` when every object of the data type must have a value for the field |
| `isReadOnly` | `true` when users cannot edit the field's values in ODM |
| `description` | Description of the field. Absent when the field has none. |
| `dictionaryAccession` | Accession of the dictionary the field's values are checked against. Absent when the field has no dictionary. |
| `dictionaryName` | Name of the dictionary the field's values are checked against. Absent when the field has no dictionary, or when you cannot read the dictionary. |

`dataType` takes these values:

| `dataType` | Applies to |
| --- | --- |
| `study` | Studies |
| `genestack:sampleObject` | Samples |
| `genestack:libraryObject` | Libraries |
| `genestack:preparationObject` | Preparations |
| `genestack:transcriptomicsParent` | Expression groups |
| `genestack:genomicsParent` | Variant groups |
| `genestack:facsParent` | Flow cytometry groups |
| `genestack:transcriptomicsObject` | Expression objects inside an expression group |
| `genestack:genomicsObject` | Variant objects inside a variant group |
| `genestack:facsObject` | Flow cytometry objects inside a flow cytometry group |

For how templates and their keys work, see [About templates](../../../contribute/templates/about-templates.md) and the [Template reference](../../../contribute/templates/template-reference.md).

## Use the accession in an import

Put the template's `id` in the import request as `templateId`:

```json
{
  "metadataLink": "https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv",
  "templateId": "GSF000123"
}
```

## Next steps

Import your study with the template. See [Import study metadata](import-study-metadata.md).
