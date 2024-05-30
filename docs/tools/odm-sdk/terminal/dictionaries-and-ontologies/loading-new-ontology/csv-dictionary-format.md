# CSV dictionary format

Custom dictionaries can be uploaded to ODM in the form of list files.
List files consist of a header line containing label or name,label. Followed by lines of dictionary terms, one per term, in the format `<label>` or `<name>,<label>`. If labels contain commas the whole label term need to be enclosed in three double quotes, “““example of label, with comma”””.

Example label only dictionary: [TherapeuticArea_Vocabulary1.csv](csv-dictionary-format/TherapeuticArea_Vocabulary1.csv)

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

Example name,label dictionary: [TherapeuticArea_Vocabulary2.csv](csv-dictionary-format/TherapeuticArea_Vocabulary2.csv)

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
