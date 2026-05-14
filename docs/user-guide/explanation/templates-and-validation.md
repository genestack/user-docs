# Templates and validation in ODM

ODM is designed to hold data from many studies, teams, and sources. Without a shared vocabulary, that data becomes very difficult to compare: one study might call a field "organism", another "species", a third "Organism (Latin name)". Templates and validation are the mechanism ODM uses to prevent that fragmentation before it happens.

## What is a template?

A **template** is a schema that defines the metadata attributes associated with a particular type of data object — Study, Sample, Expression, Variant, or Flow Cytometry. Each template specifies:

- **Name** — the canonical name of the metadata field (e.g. `Organism`, `Accession`, `Disease`).
- **Required** — whether the field must be filled in. Required fields that are blank or incorrectly filled are highlighted in red in the UI, making gaps immediately visible.
- **Metainfo type** — the data type for the field: text, integer, decimal, date, yes/no, or external link. This prevents, for example, a date being stored as free text.
- **Read-only** — whether the field can be edited after import. Some fields are intentionally locked once set.
- **Dictionary** — an optional controlled vocabulary that restricts acceptable values to a standardized list. Dictionaries are what enable cross-study harmonisation: if every study uses the same dictionary for tissue type, then tissue-based queries work reliably.
- **Description** — a hint shown to curators during metadata entry, reducing the chance of misinterpretation.

All templates also contain a set of mandatory technical fields (grayed out in the UI) that cannot be edited or removed. These include `genestack:accession` and fields required for tabular data such as `Features (string)`, `Features (numeric)`, `Values (numeric)`, and `Data Class`.

## Why templates exist

The core purpose of a template is **harmonisation**. When metadata is free-form, every curator makes independent decisions about field names, units, and vocabulary. The result is data that is internally consistent per study but incomparable across studies.

By attaching a template to a data object at import time, ODM ensures that:

1. The metadata structure is predictable and machine-readable.
2. Values in controlled-vocabulary fields come from a shared dictionary, so searches and filters work across studies.
3. Required fields are not silently omitted — gaps are surfaced immediately rather than discovered later during analysis.

Templates can be created and customised by users with the appropriate permissions, using the Template Editor application. A default template is provided out of the box, which is sufficient for many common use cases. Custom templates are appropriate when a study type requires domain-specific fields, or when institutional standards differ from the defaults.

## What validation enforces

When a template is applied to a data object, ODM performs **validation** — it checks whether the metadata in that object conforms to the rules defined by the template. Validation is triggered:

- When metadata is imported or updated via the Metadata Editor or API.
- When a template assigned to a study is changed — the validity check runs for that specific study.
- When a field in a template is edited — the validity check runs for all studies that use that template.

Validation catches several categories of problems:

- **Missing required fields** — a field marked as required that has been left blank.
- **Type mismatches** — a value that does not match the declared metainfo type (e.g. text in an integer field).
- **Out-of-vocabulary values** — a value in a dictionary-controlled field that is not in the associated dictionary.

Fields that fail validation are highlighted in red in the Metadata Editor, giving curators a clear signal of what needs to be fixed. The data can still be saved in an invalid state, but the invalid fields remain visible until corrected.

## What happens when data fails validation

Validation failure does not block import. ODM allows data to exist in an invalid state so that curators can work iteratively — import first, refine metadata afterwards. However, invalid metadata fields are flagged persistently until they are corrected, and queries that rely on those fields may not return expected results.

This design reflects a practical reality in research data management: data often arrives incomplete, and forcing complete validity at import time would make the system unusable for large, complex studies. The trade-off is that the curation process must be treated as ongoing rather than a one-time event.

## When to create a new template vs. reuse an existing one

Reuse an existing template whenever possible. Every new template is another schema that curators must be aware of, and diverging templates make cross-study comparisons harder. Before creating a new template, check whether:

- The default template covers the fields you need.
- An existing custom template in your organisation is close enough to duplicate and modify.

Create a new template (or duplicate and modify an existing one) when:

- Your study type requires fields that are not present in any existing template.
- Your organisation has a formal metadata standard that differs from what the defaults capture.
- You need a different controlled vocabulary (dictionary) for a field that already exists in another template.

Duplicating a template is the recommended starting point — it preserves the mandatory technical fields and gives you an editable copy without affecting the original.

## See also

- [Template Editor](../how-to/metadata-templates/create-template.md) — how to create, edit, and manage templates in the UI
- [Data Model](data-model.md) — overview of all foundational ODM concepts
