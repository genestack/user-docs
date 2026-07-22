---
diataxis: explanation
tab: contribute
---

# About metadata validation and curation

Validation and curation are the two processes that keep metadata trustworthy. Understanding how they relate to each other, and why ODM enforces them, helps you work more effectively with the Metadata Editor.

## What validation is

In the context of data curation, **validation** refers to the process of ensuring that metadata fields conform to predefined rules and standards set by a specific template. Each template defines a specific list of metadata fields and rules for the Study, Samples, and processed/experimental metadata tabs. When ODM checks your metadata against a template, it is asking whether the values you have provided satisfy those rules. This process is essential for maintaining the integrity, consistency, and reliability of the data within ODM.

## What curation is

Curation is the broader work that validation supports: organising, harmonising, and correcting metadata so that it conforms to the data model. Curators can not only view metadata but also validate and edit it. Validation is the mechanism that tells curators where corrections are needed; curation is the act of making those corrections.

## Why validation matters

Validation offers several concrete benefits:

- **Data quality.** Validation enforces metadata standards, ensuring that data entries are accurate, complete, and consistent. This helps maintain high data quality across studies and datasets.
- **Data harmonisation.** By using custom dictionaries and standardised terms within templates, validation aids in harmonising metadata. This makes it easier to integrate and compare data from different sources, enhancing the usability and interoperability of the data.
- **Efficiency.** Automated error detection and clear indication of invalid fields simplify the curation process. This reduces the likelihood of manual errors and saves time, making data management more efficient and reliable.

## How validation works

When you apply a template to a study, ODM continuously checks the metadata on each tab against that template's rules. If required fields are missing, contain typos, or hold values that do not match the template, an **Invalid metadata flag** appears in the upper right corner of the affected tab. The specific fields that fail validation are highlighted in red, making it straightforward to identify exactly what needs attention. For more on the Metadata Editor surface where this feedback appears, see [Metadata Editor](../../overview/navigating-the-ui/metadata-editor.md).

## Relationship to templates

The rules that drive validation come entirely from templates. A template specifies which fields are required, what data types they accept, and which controlled dictionaries apply. Without a template, there is nothing to validate against. For a full explanation of what templates are and how they are structured, see [About templates](../templates/about-templates.md).

---

To learn how to correct invalid metadata and complete a curation cycle, see [Edit and validate metadata](edit-and-validate-metadata.md).
