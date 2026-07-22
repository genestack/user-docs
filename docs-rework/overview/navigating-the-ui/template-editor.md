---
diataxis: explanation
tab: overview
---

# Template Editor

The Template Editor is the interface for creating, customizing, and updating templates. Templates define the metadata attributes that apply to data objects in ODM (Study, Sample, Expression, Variant, and Flow cytometry) and control what fields are available and required during import and curation.

## Getting there

From the Dashboard, click **Set up templates**. Alternatively, open the shortcut dock and select **Template Editor**.

## The templates list

When you open the Template Editor, you see a list of all available templates. For each template, the list shows who created it, who last updated it, and when those events occurred. Click a template name to open it and explore its attributes in detail.

## Inside a template

The per-template view presents a table of attributes, one per row. Each row shows the attribute's name, whether it is required, its metainfo type, whether it is read-only, the dictionary it draws values from (if any), and a description. Fields that are mandatory for technical reasons appear greyed out and cannot be removed or modified.

## Where to go next

If you want to understand what templates are and how they fit into the ODM data model, see [About templates](../../contribute/templates/about-templates.md). To create or edit a template, see [Create and edit a template](../../contribute/templates/create-and-edit-a-template.md). To apply a different template to an existing study, see [Change a study's template](../../contribute/templates/change-a-studys-template.md). For the full template file format and a list of mandatory fields, see the [Template reference](../../contribute/templates/template-reference.md).
