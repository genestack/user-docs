---
diataxis: reference
tab: api-libraries
---

# Curation rules reference

This reference describes the `rules.json` file format consumed by the `odm-curate-study` script. For instructions on running the script, see [Curate metadata with the curation script](curate-with-the-curation-script.md).

---

## Rule structure

A `rules.json` file is an array of mapper objects. Each object defines how raw metadata values from one or more source keys are mapped to a curated value in a target key. Values are case-sensitive.

Each mapper object accepts the following attributes:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `dictionary` | string | optional | Name of a Genestack dictionary to validate mapped values against. If a mapped value is not found in the dictionary, a warning is logged. |
| `genestack_key` | string or list | mandatory | Target metainfo key (e.g., `"Sex"`). For the key-with-unit mapper, provide a list of two keys. |
| `object_type` | string | mandatory | Target object type: `"study"` or `"sample"` (lowercase). |
| `raw_keys` | list of strings | mandatory | List of source metadata keys whose values will be looked up and mapped. |
| `rules` | object | optional | Explicit value-to-value mappings. Keys are raw values; values are the curated terms to assign. |

---

## Mapper variants

### Simple reassignment

Copies values from a raw key to the target key, with no transformation:

```json
[
    {
        "genestack_key": "Sex",
        "object_type": "sample",
        "raw_keys": ["sourceData:ae.sample.Characteristics [Sex]"]
    }
]
```

### Rules-based mapping

Translates specific raw values to curated terms. In this example, `"m"` becomes `"male"`, `"f"` becomes `"female"`, and `"?"` becomes `"unknown"`:

```json
[
    {
        "genestack_key": "Sex",
        "object_type": "sample",
        "raw_keys": ["sourceData:ae.sample.Characteristics [Sex]"],
        "rules": {
            "m": "male",
            "f": "female",
            "?": "unknown"
        }
    }
]
```

Before:

| Sex |
|-----|
| m   |
| f   |
| ?   |

After:

| Sex     |
|---------|
| male    |
| female  |
| unknown |

### Dictionary-based mapping

Validates mapped values against a dictionary's terms and synonyms. If a raw value (after any `rules` transformation) matches a synonym in the dictionary, it is replaced with the preferred term:

```json
[
    {
        "genestack_key": "Sex",
        "object_type": "sample",
        "raw_keys": ["sourceData:ae.sample.Characteristics [Sex]"],
        "dictionary": "Sex"
    }
]
```

---

## Key-with-unit mapper

For attributes whose raw values combine a numeric quantity and a unit in a single field (e.g., `"7 days"`), the key-with-unit mapper splits the value into two separate attributes.

The script uses the first whitespace character as the delimiter. Everything before the first space goes into the value attribute; everything after goes into the unit attribute. If there is no space, the entire value is placed in the value attribute and the unit attribute is left empty.

Specify `genestack_key` as a list of two keys, the first for the value and the second for the unit:

```json
[
    {
        "object_type": "sample",
        "genestack_key": ["Treatment/dose/value", "Treatment/dose/unit"],
        "raw_keys": ["Value[Dose]"],
        "dictionary": "Units - Dose/Mass/Volume"
    }
]
```

Example results:

| Sample | Raw value    | Mapped value | Mapped unit       |
|--------|--------------|--------------|-------------------|
| A      | `7 ug/ml`    | `7`          | `microgram per millilitre` (via dictionary synonym) |
| B      | `7 ug per ml`| `7`          | `ug per ml` (not found in dictionary; kept as-is) |
| C      | `7ug/ml`     | `7ug/ml`     | (empty — no space found) |

**Supported case:** Multiple values with units per sample are supported. For example, a sample with two compounds each having a dose:

| Sample Name | Medicine    | Dose   |
|-------------|-------------|--------|
| Sample      | Paracetamol | 5 mg   |
| Sample      | Analgin     | 0.5 g  |

After curation:

| Sample Name | Medicine    | Dose | Dose Unit |
|-------------|-------------|------|-----------|
| Sample      | Paracetamol | 5    | mg        |
| Sample      | Analgin     | 0.5  | g         |

**Unsupported case:** Changing a single value into multiple values for this mapper is not supported.

---

## Reassigning attributes

When the script finds a `raw_key` among the study's attributes, it reassigns the values to `genestack_key` and deletes the original `raw_key` attribute. Three cases govern this behaviour.

### Case 1: raw key is a non-template attribute, genestack key is a template attribute

Values are reassigned to `genestack_key` and `raw_key` is deleted.

Rule:

```json
[
    {
        "genestack_key": "Disease",
        "object_type": "sample",
        "raw_keys": ["Illness", "DISEASE"]
    }
]
```

Before:

| | Disease | Illness |
|-|---------|---------|
| Sample 1 | | A |
| Sample 2 | | B |

After:

| | Disease | |
|-|---------|--|
| Sample 1 | A | |
| Sample 2 | B | |

### Case 2: multiple raw keys, all non-template

When multiple `raw_keys` are specified, the script takes the value from the first non-empty raw key found for each sample. A `raw_key` that was fully reassigned (all its values moved) is deleted. A `raw_key` that was only partially reassigned (because some samples had no value for the first key and used the second instead) is retained with its remaining values.

Before:

| | Disease | Illness | DISEASE |
|-|---------|---------|---------|
| Sample 1 | | A | A1 |
| Sample 2 | | | B1 |

After (Illness fully reassigned and deleted; DISEASE partially used and retained):

| | Disease | DISEASE |
|-|---------|---------|
| Sample 1 | A | A1 |
| Sample 2 | B1 | |

This case is rare in practice. Multiple raw keys are most useful when curating across studies from different sources where the same attribute has different column names.

### Case 3: raw key is a template attribute

Template attributes cannot be deleted. When `raw_key` is a template attribute, the values are copied to `genestack_key` but `raw_key` is preserved in its original state.

Before:

| | Disease | Illness |
|-|---------|---------|
| Sample 1 | | A |
| Sample 2 | | B |

After:

| | Disease | Illness |
|-|---------|---------|
| Sample 1 | A | A |
| Sample 2 | B | B |

---

## Read-only attributes

Attributes marked as read-only in the template associated with the study cannot be curated. The `--overwrite` flag does not affect this behaviour. A warning is displayed in the logs for any read-only attribute the script encounters.

---

## Multiple rules for a single attribute

If the rules file contains more than one mapper targeting the same attribute, the script proceeds but logs a warning:

```text
Multiple curation rules were detected for the attribute X.
```

---

## Versioning (not currently supported)

A versioning feature allowing `--version-message` and `--do-not-publish` flags was documented but is currently not supported. See ODM-9665 for status.
