---
diataxis: reference
tab: overview
---

# Attached files

ODM allows users to attach arbitrary file types to studies. Attached files are stored in S3 and can be retrieved through the interface and API, but their contents are not indexed for content search. Every attached file must be assigned a [Data Class](../data-model/data-classes-reference.md) for catalogue organisation.

## Limitations

!!! danger "Requirements and limitations"
    1. An S3 bucket is mandatory to upload and work with attached files in ODM.
    2. **Export**: if an attachment's metadata was updated and got a new version, the file cannot be exported individually. Workaround: export the whole study.

## Data Class assignment

Every attached file must be assigned a Data Class at upload time (via GUI or API). This organises files within the catalogue and makes them filterable in the Study Browser. See [Data classes reference](../data-model/data-classes-reference.md) for the full list.

## Upload sources

Files can be attached from two sources:

- **Local computer**: upload directly from your machine.
- **External link**: provide an HTTP or S3 link. ODM fetches the file and copies it into the configured S3 bucket.

Attachments can be uploaded via the GUI, the `POST /api/v1/jobs/import/file` endpoint, or the `import_odm_data.py` script. Files attached without samples are also supported, useful for storing experiment design documents during early study setup.

## Supported archive formats

ODM recognises and processes `.zip` and `.gz` archives:

- **Single-file archive**: loaded as a single attachment.
- **Multi-file archive**: the archive itself is loaded as an attachment; its internal structure (contents) is parsed, stored, and displayed.
- **HDF5 inside an archive**: any HDF5 file within the archive has its structure parsed and displayed as well. See [HDF5](hdf5.md).

## Viewing and managing attachments

Attachments are displayed in the appropriate Data Class group on the **Data** tab in the Metadata Editor. Metadata can be added, edited, and customised for attachments, and additional non-template attributes can be specified. Each attached file receives a unique accession number.

## Indexing status

Indexed data files display an "Indexed Data" label with a checkmark in the interface. Attached files (which are not indexed) are shown with a different visual indicator.

## Searching for attachments

The Study Browser and API allow finding studies by attached file metadata and by Data Class. All users with access to a study can download its attached files.

## API endpoints

The following API operations are available for attached files:

1. Upload attached files
2. Find all attached files metadata
3. Find metadata of a specific attached file
4. Find studies by file ID or metadata
5. Download an attached file
6. Delete attached files

For detailed API usage, see [Import attached files](../../odm-api/contribute/import-data/import-attached-files.md) and [Search attached files](../../odm-api/explore/search-attached-files.md).
