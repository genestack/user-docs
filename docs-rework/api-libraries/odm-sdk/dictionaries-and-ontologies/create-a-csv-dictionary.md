---
diataxis: how-to
tab: api-libraries
---

# Create a CSV dictionary

This guide explains how to create a simple CSV-format dictionary for use in ODM.

Dictionaries can be loaded to ODM in CSV, JSON, OWL, OBO, or TTL formats. A CSV dictionary is the simplest option: a plain-text file listing one accepted term per line.

## Steps

1. Create a new file with a `.csv` extension.

2. On the first line, write `Label` as the column header.

3. Add each accepted value on its own line. For example:

    ```text
    Label
    g
    kg
    """value, continued"""
    ```

    If a label contains a comma, embed it within three double quotes: `"""example of label, with comma"""`.

    > **Note:** Values in ODM dictionaries always have String format, even when they are numeric.

4. Save the file. Once you have your CSV file, upload it to ODM using the [Load a custom ontology](load-a-custom-ontology.md) workflow.

## Related

- [CSV dictionary format reference](csv-dictionary-format-reference.md), full format specification including the `name,label` two-column variant.
- [Load a custom ontology](load-a-custom-ontology.md)
