# FACS (Flow Cytometry)

FACS (Fluorescence-Activated Cell Sorting) files represent processed (post-gating) flow cytometry data in a human-readable tabular format. ODM indexes FACS files and exposes API endpoints to search and filter by sample, cell population, readout type, marker, and value.

![FACS file example](../../supported-data/facs.png)

---

## File structure

A FACS file is a tab-delimited table. Each row represents a single measurement for a specific cell population and marker combination in a sample. The key columns are:

### Sample
A string identifying the sample. No additional extraction is applied — the value is stored as-is.

### CellPopulation
Describes cell subtypes in a hierarchical, path-like structure. Each level of the hierarchy is separated by a `/`:

```
CD45+, live/CD45+, CD3+/CD4
```

Counts at parent levels equal the sum of their children. However, marker-specific counts may not sum to the parent population total because individual cells can express multiple markers simultaneously.

### ReadoutType
Defines the type of value recorded for this row:

| Value | Description |
|-------|-------------|
| `Median` | Median fluorescence intensity of a fluorophore (decimal) |
| `Count` | Number of cells in the population (integer) |
| `Percentage` | Proportion of this population relative to its parent (decimal) |

### Marker
Identifies the protein or fluorophore measured on the cell surface (e.g., `PD-1`, `GZB`, `BV786`). Different marker names may refer to the same biological entity.

---

## Considerations

- Cell populations are hierarchical; cells may carry multiple markers simultaneously.
- Marker-level counts do not fully represent total population size due to overlapping markers.

---

## How ODM uses FACS files

ODM indexes FACS files and provides API endpoints (`GET /api/v1/as-user/omics/flow-cytometry/data`) to:

1. Find FACS objects and groups by metadata and data:
    - Run
    - Readout Type
    - Population
    - Marker
    - Value

2. Find objects and groups by Genestack Accession.

3. Find objects and groups by related entities:
    - Study
    - Samples

4. Update FACS group metadata by object ID.

---

## Limitations

[PLACEHOLDER: FACS file format specification — coming soon]
