# HDF5 (Hierarchical Data Format 5)

HDF5 is a widely used binary data format in genomic research, particularly for single-cell studies. It is designed to store large, complex datasets efficiently — making it a preferred choice for structured biological data such as gene expression matrices and cell-level metadata.

!!! info "Current support status"
    HDF5 is currently supported as an **Attached File** in ODM, with the ability to view and search by file structure (contents) only. Full parsing, search, and filtering of HDF5 data content is under development.

---

## Supported file extensions

| Extension | Description |
|---|---|
| `.h5` | Standard HDF5 file |
| `.h5ad` | AnnData-format HDF5 file (common in single-cell workflows) |
| `.h5.gz`, `.h5ad.zip` | Compressed versions of standard HDF5 files |

---

## How ODM uses HDF5 files

HDF5 files are uploaded as Attached Files within Studies. ODM does not index their data content at this stage, but provides the following capabilities:

### Viewing file structure (contents)

- **Via GUI**: File contents (the internal HDF5 group/dataset tree) are displayed on the Data tab of the Metadata Editor. Click the **Contents** button to expand the structure.
- **Via API**: File contents can be retrieved for a list of files or by unique Genestack Accession.

### Searching by file structure

Users can search via GUI and API using:

- **Unique file**: by Genestack Accession.
- **Files**:
    - By file contents fields/pathways (internal HDF5 paths).
    - By Study Genestack Accession.
- **Studies**:
    - By file contents fields/pathways.
    - By file Genestack Accession.

---

## Limitations

- HDF5 files are not indexed — data values inside the file cannot be searched or filtered.
- The file is stored as an opaque attachment in S3; only the internal HDF5 structure (group/dataset hierarchy) is exposed.
- Export of an individual HDF5 attachment is unavailable if the attachment's metadata has been updated and a new version was created. Workaround: export the entire Study.

[PLACEHOLDER: HDF5 technical format specification — coming soon]
