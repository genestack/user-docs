# How to configure metadata curation

This guide explains how to apply curation operations to cell metadata, feature metadata, or biosample metadata during a single-cell HDF5 transformation.

## Where these operations apply

Curation operations are available in the `cell_metadata`, `feature_metadata`, and per-entity settings within `biosample_metadata`. They are applied in the order listed below.

## Order of operations

### 1. Drop columns

Remove columns before any other processing:

```json
"columns_to_drop": ["taxon", "organism_id"]
```

### 2. Rename columns

Map source column names to new names:

```json
"columns_renaming_map": {
  "sample": "batch",
  "pctmt": "percentMito"
}
```

### 3. Replace specific values

Replace known values within a column:

```json
"columns_to_curate_values": {
  "sample": {
    "LGVXCTRL1": "lung_healthy_1"
  }
}
```

### 4. Fill missing values

Provide a default value for missing entries:

```json
"columns_to_fill_missing_values": {
  "batch": "unknown"
}
```

### 5. Set a constant value for all rows

Set all rows in a column to the same value. This can add new columns or overwrite existing ones:

```json
"set_column_value": {
  "sample_id": "lung_1"
}
```

## Attribute name standardisation

After all explicit column operations, the transformation applies automatic attribute name standardisation: column names that match known ODM canonical names are mapped to those names; non-standard names are converted to camelCase. This step is automatic and does not need to be configured.

For the full list of recognised column names and their ODM equivalents, see [Attribute Mapping Reference](attribute-mapping-reference.md).

## Exempt a column from standardisation

To prevent a specific column from being automatically renamed (for example, a Leiden cluster column with a decimal suffix), list it in `columns_to_preserve_name`:

```json
"columns_to_preserve_name": ["cluster_leiden_0.5"]
```

## Related

- [Configuration reference](configuration-reference.md): full parameter specifications for all curation fields.
- [Attribute Mapping Reference](attribute-mapping-reference.md): the complete mapping of known column names to ODM canonical names.
- [Ingest cell and expression data from an H5AD file](ingest-cell-and-expression.md)
