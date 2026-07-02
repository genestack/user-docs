# Available transformation images reference

Each transformation image defines what input formats it accepts and what ODM objects it produces. Use `GET /api/v1/transformations/images` to retrieve the current list of available images and their versions.

---

## metadata-basic

> **Note:** The `metadata-basic` image was introduced as an example transformation.

**Description:** Basic converter from attachment to metadata.

**Input formats:** `csv`

**Output formats:** `samples`

**Default memory:** `256Mi`

**Default volume:** `5Gi`

**Use case:** Converts a CSV file attached to a study into an ODM Sample metadata group. On success, the image converts the CSV to TSV and automatically triggers ODM's multipart sample import, creating a new Sample group linked to the same study as the source attachment.

**Example `data` field:**

```json
{
  "source": { "csv": {} },
  "destination": { "samples": {} }
}
```

For the end-to-end job workflow (create a configuration, submit a dry run, monitor, and review logs), see [How to run a transformation](how-to-run-a-transformation.md).

---

## hdf5-cells

**Description:** Import single-cell data and metadata from HDF5 format to ODM.

**Input formats:** H5AD (AnnData), 10x Genomics H5 (converted internally to H5AD before processing), Legacy 10x Genomics H5 v<3 (single-genome only; multi-genome legacy files are not supported).

**Output formats:** ODM Cell Group, Expression Group, with optional Sample, Library, and Preparation groups.

**Default memory:** `5Gi`

**Default volume:** `5Gi`

H5 files require significantly more scratch space because they are converted internally to H5AD format before processing.

For the full how-to and the `data` field schema, see the [single-cell](single-cell/single-cell-getting-started.md) subsection.

---

## Version conventions

- `latest` is an alias for the most recent stable version of an image. Use it for exploration and development.
- Specific tags (for example, `0.0.7`) pin the job to a particular image version. Use them when you need to reproduce a previous result - the exact image and version used in any job are recorded in its logs.
