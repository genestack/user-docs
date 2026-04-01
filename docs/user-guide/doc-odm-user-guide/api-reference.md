# API Reference: Single-Cell HDF5 Transformation (Processors Controller)

> **Related documentation:** For conceptual background on configurations, images, and jobs, see [About Single-Cell HDF5 Transformations in ODM](about-sc-hdf5-transformations.md). For step-by-step usage of these endpoints, see the the [Single-cell data in ODM: Getting Started](quickstart-sc.md) and [How-to Guides](how-to-sc-hdf5-transformations.md). For the configuration `data` object schema, see the [Configuration Reference](configuration-reference.md).

This reference describes all endpoints in the ODM Processors Controller API used to manage and execute single-cell HDF5 transformations. Endpoints are grouped into three resources: Transformation Configurations, Transformation Images, and Transformation Jobs.

---

## Quick Reference

| Operation | Method | Endpoint |
|---|---|---|
| List configurations | `GET` | `/api/v1/transformations/configurations` |
| Get a configuration | `GET` | `/api/v1/transformations/configurations/{id}` |
| Create a configuration | `POST` | `/api/v1/transformations/configurations` |
| Update a configuration | `PUT` | `/api/v1/transformations/configurations/{id}` |
| List images | `GET` | `/api/v1/transformations/images` |
| Submit a job | `POST` | `/api/v1/transformations/jobs` |
| Get job status | `GET` | `/api/v1/transformations/jobs/{id}` |
| Retrieve job logs | `POST` | `/api/v1/transformations/jobs/{id}/logs` |

---

## Transformation Configurations

A transformation configuration is a stored JSON document that defines how a source file should be processed. It contains a human-readable name and description alongside the `data` object, which is the full processing specification passed to the transformation image.

Configurations are independent of any particular run. The same configuration can be reused across multiple jobs and updated iteratively without affecting previous job results.

### List configurations

```
GET /api/v1/transformations/configurations
```

Returns an array of configuration objects. Each entry includes:

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique identifier for the configuration |
| `name` | string | Human-readable name |
| `description` | string | Human-readable description |

Use this endpoint to discover existing configurations before deciding to create a new one or reuse an existing one.

### Get a configuration

```
GET /api/v1/transformations/configurations/{id}
```

Returns the full configuration object, including the `data` field with all processing rules. Use this to inspect an existing configuration before deciding to update or reuse it.

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
| `name` | string | Yes | Human-readable name for this configuration |
| `description` | string | Yes | Human-readable description |
| `data` | object | Yes | The processing specification. See the [Configuration Reference](configuration-reference.md) for the full schema. |

**Example request body:**

```json
{
  "name": "minimal_config",
  "description": "Minimal transformation config for H5AD files",
  "data": {
    "file_type": "h5ad",
    "biosample_metadata": null,
    "cell_metadata": {
      "metadata_keys": {
        "obs": "metadata"
      }
    },
    "feature_metadata": {
      "metadata_keys": {
        "var": "metadata"
      }
    },
    "cell_expression": {
      "data_class": "Single-cell transcriptomics"
    }
  }
}
```

**Response:** The response object includes the `id` assigned to the new configuration. This `id` is required when submitting a job.

### Update a configuration

```
PUT /api/v1/transformations/configurations/{id}
```

Fully replaces the configuration at the given `id` with the provided content. The request body follows the same structure as `POST`. Use this after reviewing dry-run logs to apply adjustments before resubmitting a dry-run or running the full transformation.

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the configuration to update |

**Request body:** Same structure as `POST /api/v1/transformations/configurations`.

---

## Transformation Images

A transformation image is a versioned, containerized processing environment that executes the transformation logic for a specific input format. Images are managed separately from configurations, enabling version-controlled upgrades.

### List images

```
GET /api/v1/transformations/images
```

Returns an array of available image objects.

**Response fields per image:**

| Field | Description |
|---|---|
| `name` | Identifier used when referencing the image in a job (e.g. `"hdf5-cells"`) |
| `description` | Human-readable description of the image's purpose |
| `input_formats` | File formats accepted as input |
| `output_formats` | File formats produced as output |
| `version` | Version tag (e.g. `"latest"` or a specific release tag such as `"0.0.7"`) |

Use this endpoint to confirm image availability and identify the version to specify when submitting a job.

---

## Transformation Jobs

A transformation job binds a configuration and an image to one or more input file accessions and executes the processing pipeline. Each job produces an execution log and, when not in dry-run mode, creates or updates ODM objects.

### Submit a job

```
POST /api/v1/transformations/jobs
```

Creates and submits a new transformation job. The response includes the `id` of the created job, which is required for status and log queries.

**Request body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `configuration_id` | integer | Yes | ID of the transformation configuration to use |
| `dry_run` | boolean | Yes | `true` to simulate the run without writing data to ODM; `false` for a full run |
| `image_reference` | object | Yes | Specifies the image to use. Contains `name` (string) and `version` (string). |
| `input_accessions` | array of strings | Yes | ODM accessions of the input files to process |
| `volume_size` | integer | Yes | Scratch volume size in GB allocated for the job |

**`image_reference` fields:**

| Field | Type | Description |
|---|---|---|
| `name` | string | Image name. Use `"hdf5-cells"` for single-cell HDF5 transformations. |
| `version` | string | Version tag. Use `"latest"` or a specific release tag (e.g. `"0.0.7"`). |

**`volume_size` guidelines:**

| Input format | Recommended `volume_size` |
|---|---|
| H5AD | ≥ 1.4 × size of the original attachment (GB) |
| 10x H5 | ≥ 4 × size of the original attachment (GB) |

H5 files require significantly more scratch space due to the internal conversion to H5AD format.

**Example request body (dry run):**

```json
{
  "configuration_id": 42,
  "dry_run": true,
  "image_reference": {
    "name": "hdf5-cells",
    "version": "latest"
  },
  "input_accessions": ["GSF020408"],
  "volume_size": 30
}
```

**Example request body (full run):**

```json
{
  "configuration_id": 42,
  "dry_run": false,
  "image_reference": {
    "name": "hdf5-cells",
    "version": "latest"
  },
  "input_accessions": ["GSF020408"],
  "volume_size": 30
}
```

### Get job status

```
GET /api/v1/transformations/jobs/{id}
```

Returns the job object, including the current `status.state`. Repeat this request until the state reaches a terminal value before retrieving logs or proceeding to the next step.

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the job to query |

**`status.state` values:**

| State | Meaning |
|---|---|
| `RUNNING` | Job is in progress |
| `COMPLETED` | Job finished successfully |
| `FAILED` | Job encountered an error |

### Retrieve job logs

```
POST /api/v1/transformations/jobs/{id}/logs
```

Returns the log records for the specified job. Logs include:

- Configuration validation messages.
- Input file structure report (keys, data types, shapes, attribute names).
- Warnings and errors encountered during metadata extraction and curation.
- Linking validation results (dry-run only).
- Accessions of ODM objects created or updated (full run only).

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | integer | ID of the job whose logs to retrieve |

After a dry run, review the logs carefully before updating the configuration or proceeding to a full run. After a full run, the logs are the primary source of information about which ODM accessions were created.
