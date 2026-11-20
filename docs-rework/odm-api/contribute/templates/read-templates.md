---
diataxis: how-to
tab: odm-api
---

# How to read templates through the REST API

> **[BETA]** The template endpoints are in BETA and are subject to change. Backward compatibility is not guaranteed.

Study, sample, library, preparation and omics data imports take an optional `templateId`, the accession of the template ODM applies to the imported metadata. You can look at the templates in two ways:

- In the ODM user interface, the [Template Editor](../../../overview/navigating-the-ui/template-editor.md) lists the templates and shows the fields of each one.
- Through the REST API, `GET /api/v1/templates` lists the templates with their accessions. `GET /api/v1/templates/{id}` returns one template with its fields.

This article describes the REST API. For the full endpoint specification, see the [`templates` definition in Swagger](/swagger/?urls.primaryName=templates).

## List the templates

Call `GET /api/v1/templates`:

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/templates' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

The response is an array with one entry for each template:

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
      "name": "genestack:accession",
      "dataType": "genestack:sampleObject",
      "metainfoType": "com.genestack.api.metainfo.StringValue",
      "isRequired": true,
      "isReadOnly": true,
      "description": "Genestack-generated accession"
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

`fields` has the same fields as the Template Editor shows and exports, in the order of the export. The Template Editor shows them grouped by data type. The list includes the technical fields that ODM fills itself (see [Mandatory technical fields](../../../contribute/templates/template-reference.md#mandatory-technical-fields)). To leave them out, add `returnedTemplateFields=technical_excluded` to the request:

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/templates/GSF000123?returnedTemplateFields=technical_excluded' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

`returnedTemplateFields` takes two values:

- `all` returns every field. This is the default.
- `technical_excluded` leaves out every field whose name starts with `genestack:`, `Data Class` in expression, variant and flow cytometry metadata, and `Features (string)`, `Features (numeric)` and `Values (numeric)` in expression metadata.

The endpoint returns HTTP status `404` when no template has that accession, and `400` when `returnedTemplateFields` has another value.

A field has the keys of the template JSON file: `name`, `dataType`, `metainfoType`, `isRequired`, `isReadOnly`, `description` and `dictionaryName`. The [Template reference](../../../contribute/templates/template-reference.md#template-json-file-structure) describes each key and its values. A field also has `dictionaryAccession`, the accession of the dictionary that the field's values are checked against. `dictionaryAccession` and `dictionaryName` are absent when the field has no dictionary.

For how templates and their keys work, see [About templates](../../../contribute/templates/about-templates.md).

## Create a template from the response

You can upload the fields of a template as a new template with `odm-update-template` (see [Create or update a template](../../../api-libraries/odm-sdk/templates/create-or-update-a-template.md)):

1. Save the `fields` array as the template JSON file. Leave out `id`, `name`, `description` and `isDefault`, because the template JSON file is an array of fields only.
2. Remove `dictionaryAccession` from each field. The script finds the dictionary by `dictionaryName`.
3. Give the new template its name in the template settings file.

Request the fields with `returnedTemplateFields=technical_excluded` to keep the technical fields out of the file. When the file has them, the script prints that each one "is predefined and can be omitted", then adds its own copy. The script does not upload the template description.

To change an existing template, use the Template Editor (see [Create and edit a template](../../../contribute/templates/create-and-edit-a-template.md)) or the ODM SDK (see [Create or update a template](../../../api-libraries/odm-sdk/templates/create-or-update-a-template.md)).

## Apply the template in a metadata import

Put the template's `id` in the import request as `templateId`. For example, a study metadata import (see [Import study metadata](../import-data/import-study-metadata.md)) takes this body:

```json
{
  "metadataLink": "https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv",
  "templateId": "GSF000123"
}
```
