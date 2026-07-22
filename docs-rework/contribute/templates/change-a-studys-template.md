---
diataxis: how-to
tab: contribute
---

# How to change a study's template

This guide explains how to apply a different template to a study in the Metadata Editor.

## Prerequisites

- You must be a member of the Curator group to change a study's template.
- The target template must already exist in ODM. If you need to create one, see [Create and edit a template](create-and-edit-a-template.md).

## Steps

1. Open the study in the Metadata Editor.
2. Click the study name at the top of the page. A dropdown menu appears.
3. Select **Apply another**.
4. A list of available templates appears. Hover over any template name to reveal the **Explore** option, which opens that template in the Template Editor so you can inspect it before committing.
5. Select the template you want to apply.
6. Confirm the selection when prompted.

## What happens next

After you confirm, ODM automatically runs a validity check for that specific study against the new template. Any attribute that does not match the new template is flagged as invalid. Attributes that were not controlled by the previous template and are not controlled by the new one are preserved as non-template-controlled fields. They remain in the study but are not validated.

To understand validity check behaviour in detail, see [Template reference](template-reference.md). To resolve invalid metadata that the check surfaces, see [Edit and validate metadata](../curate-metadata/edit-and-validate-metadata.md).

> **Note:** if you change the *default* template (the one that ODM applies to all new studies by default), the validity check runs across all studies that currently use that template, not just the one you are editing.
