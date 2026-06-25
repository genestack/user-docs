# Available transformation images reference

Each transformation image handles a specific input/output format pair. Use `GET /api/v1/transformations/images` to retrieve the current list of available images and their versions at runtime.

---

## metadata-basic

> **Note:** The `metadata-basic` image was introduced as an example transformation.

**Description:** Basic converter from attachment to metadata.

**Input formats:** `csv`

**Output formats:** `samples`

**Default memory:** `256Mi`

**Default volume:** `5Gi`

**Available versions:** `latest`

**Use case:** Converts a CSV file attached to a study into an ODM Sample metadata group. The configuration `data` field specifies the source format and the destination entity type.

**Example `data` field:**

```json
{
  "source": { "csv": {} },
  "destination": { "samples": {} }
}
```

For the full how-to, see [csv-to-tsv/how-to-transform-csv-to-tsv.md](csv-to-tsv/how-to-transform-csv-to-tsv.md).

---

## hdf5-cells

**Description:** Import single-cell data and metadata from HDF5 format to ODM.

**Input formats:** H5AD (AnnData), 10x Genomics H5 (converted internally to H5AD before processing), Legacy 10x Genomics H5 v<3 (single-genome only; multi-genome legacy files are not supported).

**Output formats:** ODM Cell Group, Expression Group, and attachments, with optional Sample, Library, and Preparation groups.

**Default memory:** `5Gi`

**Default volume:** `5Gi`

**Available versions:** `latest`

H5 files require significantly more scratch space because they are converted internally to H5AD format before processing.

For the full how-to and the `data` field schema, see the [single-cell](single-cell/single-cell-getting-started.md) subsection.

---

## Version conventions

- `latest` is an alias for the most recent stable version of an image. Use it for exploration and development.
- Specific tags (for example, `0.0.7`) pin the job to a particular image version. Use them in production pipelines where reproducibility matters.

---

## Known limitations

Only one transformation process can be run per attachment.

!!! warning "Editorial TODO: resolve before publishing"
    Verify: the one-transformation-per-attachment constraint is not present in transformation-images-develop/. Confirm against another source (e.g. the attachment-transformation.md migration source or the Applications layer) before treating it as authoritative.
