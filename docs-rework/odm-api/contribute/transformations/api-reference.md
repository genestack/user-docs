---
sources:
  - path: docs/user-guide/doc-odm-user-guide/api-reference.md
    lines: [1, 256]
diataxis: reference
tab: odm-api
task: task-094
tickets:
  - ODM-13233
  - ODM-13239
  - ODM-13243
  - ODM-13292
  - ODM-13304
  - ODM-13324
  - ODM-13326
---

# Processors Controller API reference

This reference describes the Processors Controller API endpoints used to manage transformation configurations, list images, and submit, monitor, and inspect transformation jobs. The endpoints are use-case-agnostic — they apply to all transformation types.

For the conceptual model behind these endpoints, see [About the Processors Controller](about-processors-controller.md). For the step-by-step workflow, see [How to run a transformation](how-to-run-a-transformation.md). For per-image `data` field schemas, see [Available images reference](available-images-reference.md) and [Single-cell HDF5 configuration reference](single-cell/configuration-reference.md).

---

## Quick reference

| Operation | Method | Endpoint |
|---|---|---|
| List configurations | `GET` | `/api/v1/transformations/configurations` |
| Get a configuration | `GET` | `/api/v1/transformations/configurations/{id}` |
| Create a configuration | `POST` | `/api/v1/transformations/configurations` |
| Update a configuration (creates a new version) | `PUT` | `/api/v1/transformations/configurations/{id}` |
| List configuration versions | `GET` | `/api/v1/transformations/configurations/{id}/versions` |
| Get a configuration version | `GET` | `/api/v1/transformations/configurations/{id}/versions/{version}` |
| List images | `GET` | `/api/v1/transformations/images` |
| Submit a job | `POST` | `/api/v1/transformations/jobs` |
| List jobs | `GET` | `/api/v1/transformations/jobs` |
| Get job status | `GET` | `/api/v1/transformations/jobs/{id}` |
| Cancel a job | `POST` | `/api/v1/transformations/jobs/{id}/cancel` |
| Retrieve job logs | `POST` | `/api/v1/transformations/jobs/{id}/logs` |

---

## Pagination

All list (collection) endpoints return a paginated envelope rather than a bare array, and accept `limit` and `offset` query parameters. The paginated endpoints are:

- `GET /api/v1/transformations/configurations`
- `GET /api/v1/transformations/configurations/{id}/versions`
- `GET /api/v1/transformations/jobs`
- `GET /api/v1/transformations/images`

**Query parameters:**

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `limit` | integer | 100 | min 1, max 1000 | Maximum number of items to return. |
| `offset` | integer | 0 | min 0 | Number of items to skip from the start of the list. |

Both parameters are optional; the defaults apply when omitted.

**Response envelope:**

```json
{
  "items": [ ... ],
  "total": 137,
  "limit": 100,
  "offset": 0
}
```

| Field | Type | Description |
|---|---|---|
| `items` | array | The page of results. Always an array — empty rather than `null`. |
| `total` | integer | Total number of items available before pagination. |
| `limit` | integer | The effective limit applied to this page. |
| `offset` | integer | The effective offset applied to this page. |

> **[Breaking change]** List endpoints previously returned a bare JSON array; they now return the paginated envelope above, with results under `items`.

---

## Transformation configurations

A transformation configuration is a stored JSON document that defines how a source file is processed. Configurations are reusable across jobs and versioned. For the conceptual model, see [About the Processors Controller](about-processors-controller.md); versioning behaviour is described under [Update a configuration](#update-a-configuration) below.

### List configurations

```
GET /api/v1/transformations/configurations
```

Returns a [paginated envelope](#pagination); each `items` entry is the latest version of a configuration, including its full `data`. Each object includes:

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique identifier for the configuration |
| `version` | integer | Version number returned (the latest version of the configuration) |
| `name` | string | Human-readable name |
| `description` | string | Human-readable description |
| `data` | object | The full processing specification (image-specific) |
| `create_time` | string | Timestamp of when the configuration was created (e.g. `2026-04-14T15:27:04Z`) |

### Get a configuration

```
GET /api/v1/transformations/configurations/{id}
```

Returns the latest version of the configuration with the given `id`, including the `data` field with all processing rules. The response includes a `create_time` timestamp recording when the configuration was created, and a `version` field alongside `id` identifying which version was returned. To retrieve an earlier version, use the version endpoints below.

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the configuration to retrieve |

### Create a configuration

```
POST /api/v1/transformations/configurations
```

Creates a new transformation configuration and returns its assigned `id`.

**Request body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | No | Human-readable name (optional but recommended) |
| `description` | string | No | Human-readable description (optional but recommended) |
| `data` | object | Yes | The processing specification. The schema is image-specific — see [Available images reference](available-images-reference.md). |

**Response:** A reference object containing the `id` assigned to the new configuration (and its `version`, which is `1` for a new configuration). This `id` is required when submitting a job.

### Update a configuration

```
PUT /api/v1/transformations/configurations/{id}
```

Creates a new version of the configuration at the given `id`. The current state is archived as a previous version and the active version is incremented; the configuration is not overwritten. Earlier versions remain retrievable through the version endpoints below.

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the configuration to update |

**Request body:** Same structure as `POST /api/v1/transformations/configurations`.

### List configuration versions

```
GET /api/v1/transformations/configurations/{id}/versions
```

Returns a [paginated envelope](#pagination) whose `items` are the available versions of the configuration with the given `id`.

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the configuration whose versions to list |

### Get a configuration version

```
GET /api/v1/transformations/configurations/{id}/versions/{version}
```

Returns a single configuration version.

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the configuration |
| `version` | integer | Version to retrieve |

---

## Transformation images

A transformation image is a versioned, containerised processing environment that executes the transformation logic for a specific input format, and is managed separately from configurations.

### List images

```
GET /api/v1/transformations/images
```

Returns a [paginated envelope](#pagination) whose `items` are the available image objects.

**Response fields per image:**

| Field | Description |
|---|---|
| `name` | Identifier used when referencing the image in a job (e.g. `"hdf5-cells"`) |
| `version` | Version tag (e.g. `"latest"` or a specific release tag such as `"0.0.7"`) |
| `description` | Human-readable description of the image's purpose |
| `input_formats` | File formats accepted as input |
| `output_formats` | File formats produced as output (one of: `attachments`, `cells`, `expressions`, `flow-cytometries`, `libraries`, `preparations`, `samples`, `studies`, `variants`) |
| `default_volume_size` | Default scratch volume size used when a job omits `volume_size` (Kubernetes quantity string, e.g. `"30Gi"`) |
| `default_memory_size` | Default memory limit used when a job omits `memory_size` (Kubernetes quantity string, e.g. `"512Mi"`) |

---

## Transformation jobs

A transformation job binds a configuration and an image to one or more input file accessions and executes the processing pipeline, producing an execution log and, on a full (non-dry-run) run, creating or updating ODM objects.

Every job is retained permanently. Once a job finishes — or is cancelled — its final status and full logs are kept in long-term storage and stay available through these endpoints, while its compute resources are freed. Jobs cannot be deleted.

### Access and permissions

Every transformation job endpoint enforces an access check against the studies that contain the attachments in the job's `input_accessions`. Every study that contains a listed attachment must be **shared with you**. If the attachments span multiple studies, all of those studies must be shared with you.

If any accession is not found, or belongs to a study that is not shared with you, the request is rejected with a generic message — `Item not found or insufficient permission` — that does not reveal whether the item exists.

Creating or cancelling a job additionally requires **Curator group membership**. Jobs cannot be deleted; they are retained permanently.

On submission (`POST /api/v1/transformations/jobs`), the accessions to check are taken from the request body. For the other endpoints, ODM retrieves the job's `input_accessions` (via `GET /api/v1/transformations/jobs/{id}`) and checks that the studies that contain them are shared with you.

For how studies are shared, see [Sharing and ownership](../../../overview/access-control/sharing-and-ownership.md); for the Curator group, see [Groups and roles](../../../overview/access-control/groups-and-roles.md).

| Endpoint | Required access |
|---|---|
| `GET /api/v1/transformations/jobs` | Every study containing a listed input attachment is shared with you. Results are filtered to the jobs you can access. |
| `GET /api/v1/transformations/jobs/{id}` | Every study containing a listed input attachment is shared with you |
| `POST /api/v1/transformations/jobs/{id}/logs` | Every study containing a listed input attachment is shared with you |
| `POST /api/v1/transformations/jobs` | Curator group membership + every study containing a listed input attachment is shared with you |
| `POST /api/v1/transformations/jobs/{id}/cancel` | Curator group membership + every study containing a listed input attachment is shared with you |

### Submit a job

```
POST /api/v1/transformations/jobs
```

Creates and submits a new transformation job. The response includes the `id` of the created job.

**Request body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `configuration_reference` | object | No | The transformation configuration to use. Contains `id` (integer, required within the object) and `version` (integer, optional). Optional at the API level, though most images require a configuration. If omitted, the latest version is used (see below). |
| `dry_run` | boolean | No | `true` to simulate without writing data; `false` (the default) for a full run |
| `image_reference` | object | Yes | Specifies the image to use. Contains `name` (string) and `version` (string). |
| `input_accessions` | array of strings | Yes | ODM accessions of the input files to process (at least one) |
| `volume_size` | string | No | Scratch volume size as a Kubernetes quantity string (e.g. `"30Gi"`). If omitted, the image's `default_volume_size` is used, falling back to `"30Gi"`. |
| `memory_size` | string | No | Memory limit as a Kubernetes quantity string (e.g. `"512Mi"`). If omitted, the image's `default_memory_size` is used, falling back to `"512Mi"`. |

**`configuration_reference` fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | ID of the transformation configuration |
| `version` | integer | No | Specific configuration version to run. If omitted, the latest version is used. |

The job records the configuration version it executed against, so the audit trail remains intact even if the configuration is updated later.

> **[Subject to change — ODM-13233]** The exact name and shape of the job-submission `configuration_reference` field are not yet finalized. This block documents the proposed schema; verify against the released API before relying on it.

**`image_reference` fields:**

| Field | Type | Description |
|---|---|---|
| `name` | string | Image name (e.g. `"hdf5-cells"` or `"metadata-basic"`) |
| `version` | string | Version tag. Use `"latest"` or a specific release tag (e.g. `"0.0.7"`). |

For `volume_size` sizing guidance — including the per-format recommendations and why 10x H5 files need extra scratch space — see [Job resource parameters reference](resource-parameters-reference.md). For per-image guidance, see [Available images reference](available-images-reference.md).

### List jobs

```
GET /api/v1/transformations/jobs
```

Returns a [paginated envelope](#pagination). Each object in `items` includes the same fields as the single-job response (see [Get job status](#get-job-status)), including `create_time` and `end_time`. Results are filtered to the jobs whose input attachments you can access; see [Access and permissions](#access-and-permissions).

> **Note — pagination counts and access filtering:** The service paginates *before* per-user access filtering is applied, so the pagination metadata describes the unfiltered dataset, not what you can see. `items` is the access-filtered subset of the requested page, but `total`, `limit`, and `offset` are passed through unmodified and reflect all jobs matching the query — including jobs you cannot access. As a result, `total` can overcount, a page may return fewer than `limit` items (even zero) while accessible jobs still exist on later pages, and a page count derived as `ceil(total / limit)` will be wrong. Do not assume `items.length == limit` on a full page, nor that `total` equals the number of jobs you can access.

### Get job status

```
GET /api/v1/transformations/jobs/{id}
```

Returns the job object, including the current `status.state`.

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the job to query |

**`status.state` values:**

| State | Meaning |
|---|---|
| `PENDING` | Job accepted; its processing environment has not started being set up yet |
| `WAITING` | Processing environment is starting up, typically while the transformation image is downloaded; the transformation has not begun |
| `RUNNING` | Transformation is actively processing the input |
| `DONE` | Finished successfully |
| `FAILED` | Finished with an error (may carry a reason such as `OOMKilled`) |
| `CANCELLED` | Cancelled by a user; a terminal state distinct from `FAILED`, carrying no reason or description |
| `UNKNOWN` | The job's state cannot currently be determined |

For a normal run the order is `PENDING` → `WAITING` → `RUNNING` → `DONE` (or `FAILED`).

**`archived`:**

A required boolean indicating whether the job has finished and its final status and full logs have been moved to permanent storage (and its compute resources freed). Archived jobs can no longer be cancelled, but their status and logs remain available. `archived` is `false` while a job is running and flips to `true` a short time after it finishes — or immediately when it is cancelled. This field is present on both this response and [List jobs](#list-jobs).

**`end_time`:**

The job object includes an `end_time` timestamp, set automatically when the job reaches a terminal state (`DONE`, `FAILED`, or `CANCELLED`). While the job is in a non-terminal state (`PENDING`, `WAITING`, `RUNNING`, or `UNKNOWN`), `end_time` is omitted. Pair it with `create_time` to calculate how long a job ran. The field is populated for existing jobs as well as new ones.

### Retrieve job logs

```
POST /api/v1/transformations/jobs/{id}/logs
```

Returns the log records for the specified job. Logs are always available, including for finished and archived jobs: while the job runs, the endpoint returns its live logs; once the job has been archived, it serves the stored logs transparently. A finished or archived job's logs are never reported as not found. The `tail_lines` option applies to both live and archived logs.

Logs include:

- Configuration validation messages.
- Input file structure report (keys, data types, shapes, attribute names).
- Warnings and errors encountered during metadata extraction and curation.
- Linking validation results (dry-run).
- Accessions of ODM objects created or updated (full run).

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the job whose logs to retrieve |

### Cancel a job

```
POST /api/v1/transformations/jobs/{id}/cancel
```

Cancels a running job. Cancellation terminates the job immediately, records it in the terminal `CANCELLED` state, and archives its final status and logs to permanent storage. The endpoint takes no request body and returns `204 No Content`.

A job can be cancelled until it has been archived. Once archived (its compute resources freed), the endpoint returns a not-found error; its status and logs remain available.

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the job to cancel |

Requires Curator group membership, and every study containing a listed input attachment must be shared with you. See [Access and permissions](#access-and-permissions).
