---
diataxis: explanation
tab: api-libraries
---

# About dictionaries and ontologies

Dictionaries in ODM are controlled vocabularies used for metadata validation. When a template field specifies a dictionary, values entered for that field are validated against the dictionary's terms and synonyms. This is how ODM enforces consistent, harmonised metadata across studies.

## What dictionaries are

A dictionary is a list of accepted terms: words or phrases that are valid values for a metadata attribute. Dictionaries range from simple flat lists (a CSV file of labels) to full ontological hierarchies (OWL, OBO, TTL, or JSON files). SKOS-encoded vocabularies in RDF/XML or TURTLE format are also supported and enable hierarchical browsing within the platform.

Uploading a dictionary with the same name as an existing dictionary creates a new version of that dictionary. The system marks the previous version as obsolete, which is highlighted in red in the Template Editor. Existing templates that reference the old version must be updated to use the new one.

## How dictionaries are used in metadata curation

A template can associate any of its attributes with a dictionary. During curation, whether through the UI or via the curation script, values for that attribute are looked up against the dictionary's terms and synonyms and, if matched, replaced with the preferred term. For more on how curation works, see the contribute documentation on [validation and curation](../../../contribute/curate-metadata/about-validation-and-curation.md).

## ODM default dictionaries

ODM ships with a curated set of standard bioinformatics ontologies loaded at installation, covering taxonomy, cell types, diseases, anatomy, experimental factors, and many units vocabularies. See [Default dictionaries reference](default-dictionaries-reference.md) for the full list.

## Custom dictionaries

Organisations can load their own dictionaries to extend or override the defaults. Two loading workflows are available:

- Load an ontology file (OWL, OBO, TTL, JSON, or SKOS). See [Load a custom ontology](load-a-custom-ontology.md).
- Create a simple CSV list. See [Create a CSV dictionary](create-a-csv-dictionary.md).

## Supported formats

ODM accepts dictionaries in the following formats:

- **CSV**, a flat list of labels, or name+label pairs. See [CSV dictionary format reference](csv-dictionary-format-reference.md).
- **JSON, OWL, OBO, TTL**, standard ontology serialisation formats.
- **SKOS** (RDF/XML or TURTLE), hierarchical vocabularies supporting term-tree browsing within ODM. See the SKOS dictionary reference.

## Related

- [Default dictionaries reference](default-dictionaries-reference.md)
- [CSV dictionary format reference](csv-dictionary-format-reference.md)
- [Load a custom ontology](load-a-custom-ontology.md)
- [Create a CSV dictionary](create-a-csv-dictionary.md)
- [Templates](../../../contribute/templates/index.md)
