---
diataxis: reference
tab: contribute
---

# Template reference

This reference describes the template file format and the behaviour that governs template application and validation. The same format applies to templates created or exported through the Template Editor and to templates loaded via the ODM SDK.

## Template JSON file structure

A template JSON file is an array of attribute objects. Each object defines one metadata attribute with these keys:

| Key | Required | Description |
| --- | --- | --- |
| `name` | Yes | Attribute name as it appears in the Metadata Editor, unique within its data type |
| `dataType` | Yes | Data type the attribute applies to. See the values below. |
| `metainfoType` | Yes | Type of the attribute's values. See the values below. No value bounds can be set. |
| `isRequired` | Yes | When `true`, the Metadata Editor marks the attribute as invalid when it is blank or its value is wrong. |
| `isReadOnly` | No | When `true`, curators cannot edit the attribute's values. |
| `description` | No | Hint text shown to curators during metadata entry, at most 500 characters |
| `dictionaryName` | No | Name of the dictionary the attribute's values are checked against. See [Load a custom ontology](../../api-libraries/odm-sdk/dictionaries-and-ontologies/load-a-custom-ontology.md). |

`dataType` takes these values:

| `dataType` | Applies to |
| --- | --- |
| `study` | Studies |
| `genestack:sampleObject` | Samples |
| `genestack:libraryObject` | Libraries |
| `genestack:preparationObject` | Preparations |
| `genestack:transcriptomicsParent` | Expression metadata |
| `genestack:genomicsParent` | Variant metadata |
| `genestack:facsParent` | Flow cytometry metadata |

`metainfoType` takes these values:

| `metainfoType` | Values |
| --- | --- |
| `com.genestack.api.metainfo.StringValue` | Text |
| `com.genestack.api.metainfo.IntegerValue` | A whole number |
| `com.genestack.api.metainfo.DecimalValue` | A number |
| `com.genestack.api.metainfo.BooleanValue` | `true` or `false` |
| `com.genestack.api.metainfo.DateTimeValue` | A date, with or without a time |
| `com.genestack.api.metainfo.ExternalLink` | A URL |

### Example attribute object

```json
{
  "dataType": "genestack:sampleObject",
  "name": "Organism",
  "metainfoType": "com.genestack.api.metainfo.StringValue",
  "dictionaryName": "NCBI Taxonomy",
  "isRequired": true,
  "isReadOnly": false,
  "description": "The organism from which the sample was derived."
}
```

## Field grouping

Prefix an attribute `name` with a common header and a `/` character to nest attributes under that header in the Metadata Editor. For example, `"Sample characteristics/Age"` and `"Sample characteristics/Sex"` both appear under the `Sample characteristics` group.

## Attribute order

The order of attribute objects in the template JSON file is preserved exactly in the Metadata Editor UI.

## Mandatory technical fields

All templates contain mandatory technical fields. These fields are shown in grey in the Template Editor and cannot be edited or removed. Attempts to add or modify them through the SDK produce the errors described in [Technical field errors](#technical-field-errors) below.

**Common field (all entity types):**

- `genestack:accession`: automatically added for all object types listed under `dataType` above.

**Tabular data fields** (Tabular, Variants, and Flow Cytometry data):

- `Features (string)`
- `Features (numeric)`
- `Values (numeric)`
- `Data Class`

## Template settings file

When loading a template via the ODM SDK, you provide a `template_settings.json` file alongside the template JSON. This file controls how the template is registered in ODM:

```json
{
    "template_path": "Default_ODM_Template.json",
    "template_name": "Default Template",
    "replace": true,
    "mark_default": false
}
```

`template_path`: path to the template JSON file.

`template_name`: the name the template will have in ODM.

`replace`: when `true`, an existing template with the same name is overwritten.

`mark_default`: when `true`, this template becomes the new default template for the organisation.

## Validity check behaviour

A validity check runs automatically whenever a template is applied or a template field is modified.

**Changing a template assigned to a study:** the validity check runs only for that specific study.

**Editing a field in a template:** the validity check runs for all studies that currently use that template.

## Technical field errors

These apply when using the SDK to load templates that include technical fields.

**If a technical field is added manually to the template JSON:**

> *Template field "genestack:accession" of type "{data_type}" is predefined and can be omitted.*

The script continues. The manually-specified field is ignored and the automatically-added version is used.

**If a technical field is edited:**

> *Template field "genestack:accession" of type "{data_type}" is predefined and cannot be edited.*

The script stops.

The same behaviour and error messages apply to `Features (string)`, `Features (numeric)`, `Values (numeric)`, and `Data Class`.

## Export note

When you export a template from the Template Editor, the exported JSON uses the current field name `genestack:accession`. Prior to release 1.61, the exported field was named `Accession`.
