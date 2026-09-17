---
diataxis: reference
tab: api-libraries
---

# CSV dictionary format reference

Custom dictionaries can be uploaded to ODM as CSV list files. A list file consists of a header line specifying the column structure, followed by one term per line.

Two header formats are supported:

- `label`, a single-column file where each line is the display label for the term.
- `name,label`, a two-column file where each line provides a short code (`name`) and a display label (`label`).

If a label contains a comma, wrap the entire label in three double quotes: `"""example of label, with comma"""`.

## Example: label-only dictionary

[TherapeuticArea_Vocabulary1.csv](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/loading-new-ontology/csv-dictionary-format/TherapeuticArea_Vocabulary1.csv)

```text
label
"""Cardiovascular, Renal and Metabolism [CVRM]"""
Gastrointestinal [GI]
Infection [INFEC]
Autoimmune [AI]
Neuroscience [NEURO]
Oncology [ONC]
Immuno-oncology [IMMUONC]
Inflammation [INFLA]
Respiratory [RESP]
Vaccines [VA]
```

## Example: name,label dictionary

[TherapeuticArea_Vocabulary2.csv](../../../assets/tools/odm-sdk/terminal/dictionaries-and-ontologies/loading-new-ontology/csv-dictionary-format/TherapeuticArea_Vocabulary2.csv)

```text
name,label
[CVRM],"""Cardiovascular, Renal and Metabolism"""
[GI],Gastrointestinal
[INFEC],Infection
[AI],Autoimmune
[NEURO],Neuroscience
[ONC],Oncology
[IMMUONC],Immuno-oncology
[INFLA],Inflammation
[RESP],Respiratory
[VA],Vaccines
```

## Related

- [About dictionaries and ontologies](about-dictionaries.md)
- [Load a custom ontology](load-a-custom-ontology.md)
