# How to create new simple dictionary

Dictionaries can be loaded to ODM in CSV, JSON, OWL, OBO or TTL formats. In order to create a simple CSV format dictionary create a file in CSV format, add “Label” to the first line and then add each value one per line. Note labels with commas must be embedded within three double quotes.

For example:

```text
Label
g
kg
"""value, continued"""
```

Example of .csv file:

[body_weight_unit.csv](body_weight_unit.csv)

!!! note
    Please note that values in dictionary always have String format in ODM, even if they are numbers.
