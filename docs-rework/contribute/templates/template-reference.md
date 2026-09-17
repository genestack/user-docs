---
diataxis: reference
tab: contribute
---

# Template reference

This reference describes the template file format and the behaviour that governs template application and validation. The same format applies to templates created or exported through the Template Editor and to templates loaded via the ODM SDK.

## Template JSON file structure

A template JSON file is an array of attribute objects. Each object defines one metadata attribute and must contain the following keys:

`dataType`: the ODM entity type the attribute applies to. Accepted values:

- `"study"`
- `"genestack:sampleObject"`
- `"genestack:libraryObject"`
- `"genestack:preparationObject"`
- `"genestack:facsParent"`
- `"genestack:genomicsParent"`
- `"genestack:transcriptomicsParent"`

`name`: the attribute name as it appears in the Metadata Editor.

`metainfoType`: the data type of the attribute value. Must be one of:

- `"com.genestack.api.metainfo.IntegerValue"`: use for INT values
- `"com.genestack.api.metainfo.DecimalValue"`: use for FLOAT values
- `"com.genestack.api.metainfo.StringValue"`
- `"com.genestack.api.metainfo.BooleanValue"`
- `"com.genestack.api.metainfo.DateTimeValue"`: use for DATE or TIME values
- `"com.genestack.api.metainfo.ExternalLink"`

No value bounds can be set currently.

`dictionaryName`: (optional) the name of a controlled vocabulary to validate the attribute against. See [Load a custom ontology](../../api-libraries/odm-sdk/dictionaries-and-ontologies/load-a-custom-ontology.md).

`isRequired`: boolean. When `true`, leaving this attribute blank or filling it incorrectly causes it to be highlighted as invalid in the Metadata Editor.

`isReadOnly`: boolean. When `true`, the attribute cannot be edited by curators.

`description`: a hint text shown to curators during metadata entry. Maximum 500 characters.

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
