# Attached Files

ODM allows users to upload and manage any file type as an attachment within a Study. Attached files are stored in S3 but are **not indexed** — their content cannot be searched or filtered. Searches against attached files use metadata only.

---

## Overview

Attached files are distinct from imported (indexed) data such as Expression, Variant, or Flow Cytometry objects. They have a separate workflow and dedicated API endpoints; attached files cannot be accessed via expression, variant, or flow cytometry data endpoints.

!!! note "Importing vs. attaching"
    You can attach a valid expression matrix to a Study as an attached file. However, it will not be initialized or indexed. Such files are not accessible via expression endpoints and cannot be searched by data values.

Every uploaded attachment **must be assigned a Data Class** to ensure proper organization within the catalogue.

---

## Prerequisites

!!! danger "S3 bucket required"
    An S3 bucket is mandatory to upload and work with the Attached Files functionality in ODM.

---

## Uploading attachments

Attachments can be uploaded via:

- **GUI** — drag-and-drop or file picker within a Study.
- **API** — `POST /api/v1/jobs/import/file` (job endpoints).
- **CLI** — the `import_odm_data.py` script.

All uploaded attachments are stored in S3 and reflected in the system immediately after upload.

---

## Managing and viewing attachments

Attachments are displayed in the appropriate Data Class group on the **Data** tab in the User Interface. From there you can:

- View and manage uploaded files.
- Add, edit, and customize metadata for individual attachments.
- Specify additional non-template attributes.

---

## Searching for attachments

- **Study Browser**: find Studies by attached file metadata, or by the Data Class assigned to attached files.
- **API**: find Studies by attached file ID or metadata (metadata search only; data content is not indexed).

---

## API endpoints

| Operation | Endpoint |
|---|---|
| Upload an attached file | `POST /api/v1/jobs/import/file` |
| List all attached files and their metadata | `GET /api/v1/as-user/files` |
| Get metadata for a specific attached file | `GET /api/v1/as-user/files/{id}` |
| List attached files for a Study | `GET /api/v1/as-user/integration/link/files/by/study/{id}` |
| Find Studies by attached file ID or metadata | Study search endpoints with file filters |
| Download an attached file | File download endpoint |
| Delete attached files | File deletion endpoint |

!!! note "Permissions"
    To search for or retrieve attached files, the Study must be shared with you. If a Study has no attached files, the API returns an empty array `[]`.

### Example: listing attached files for a Study

```bash
curl -X 'GET' \
  'https://<HOST>/api/v1/as-user/integration/link/files/by/study/GSF1280195?includeContents=false' \
  -H 'accept: application/json' \
  -H 'Genestack-API-Token: <TOKEN>'
```

Response:

```json
[
  {
    "genestack:accession": "GSF1283030",
    "genestack:name": "AsnicarF_2017_sample.pdf",
    "Data Class": "Other"
  }
]
```

---

## Limitations

1. An S3 bucket is mandatory for all Attached Files functionality.
2. **Export limitation**: if an attachment's metadata has been updated (creating a new version), the attachment itself cannot be exported individually. Workaround: export the entire Study. This is being addressed in a future release.
