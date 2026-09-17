---
diataxis: how-to
tab: api-libraries
---

# How to create or update a template

This guide explains how to upload a custom template from a local computer into ODM, or update an existing template, using the `odm-update-template` script.

Templates loaded through the SDK are available to all users on the instance.

## Prerequisites

- Configured ODM SDK. See [Configure](../configure.md).
- "Set up templates" permission and a Bearer token or API token. See [Authentication and tokens](../../../odm-api/getting-started/authentication-and-tokens.md).
- A template JSON file. See the [Template reference](../../../contribute/templates/template-reference.md) for the file format.
- A template settings JSON file (for example, `default_ODM_template_settings.json`).

For the equivalent operation through the ODM user interface, see [Create and edit a template](../../../contribute/templates/create-and-edit-a-template.md).

## Steps

1. Download or create your template JSON file. The file contains an array of field definitions with rules for each attribute. For the structure, see the [Template reference](../../../contribute/templates/template-reference.md).

2. Download a template settings JSON file. Edit it to match your intended upload:

    ```json
    {
      "template_path": "/PATHTOTEMPLATEFILE/Default_ODM_Template.json",
      "template_name": "Default Template",
      "replace": true,
      "mark_default": false
    }
    ```

    - `template_path`, path to your template JSON file.
    - `template_name`, name that will appear in ODM.
    - `replace`, if `true`, replaces any existing template with the same name.
    - `mark_default`, if `true`, marks this template as the new organisation-wide default.

3. Run the script:

    ```shell
    odm-update-template -H GENESTACK_ENDPOINT_ADDR /PATHTOSETTINGSFILE/default_ODM_template_settings.json
    ```

    Where `GENESTACK_ENDPOINT_ADDR` is the URL of your ODM instance.

4. Verify: open the Template Editor in ODM and confirm the template appears in the list.

## Explore script options

```shell
odm-update-template -h
```

## Related

- [Delete a template](delete-a-template.md)
- [Template reference](../../../contribute/templates/template-reference.md)
