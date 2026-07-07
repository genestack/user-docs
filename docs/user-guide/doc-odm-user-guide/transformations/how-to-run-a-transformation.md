# How to run a transformation

This guide covers the end-to-end steps to run a transformation job in ODM using the Processors Controller API. The process is the same regardless of which image you use: create or identify a configuration, submit a dry-run job to validate, review the logs, then submit the full run.

For a conceptual overview of configurations, images, and jobs, see [About the Processors Controller](about-processors-controller.md).

## Prerequisites

- An API token. See [Authentication and tokens](../getting-a-genestack-api-token.md).
- Curator group membership.
- Every study that contains an attachment listed in the job's `input_accessions` must be shared with you. If a request references an attachment that does not exist or is not shared with you, it is rejected with a `422 Unprocessable Entity` response whose message names the affected accessions, for example: `The following input accessions were not found or are not shared with you: GSFXXX.`
- The source attachment already uploaded to a study in ODM (you need its accession). See [Import attached files](../import-data-in-odm.md#attach-a-file).

## Step 1: Identify the right image

List available transformation images:

```
GET /api/v1/transformations/images
```

Note the `name` and `version` of the image you want to use. The `version` field is optional - if omitted or set to `"latest"`, the most recent version is used automatically. Specify an explicit version tag (for example, `"0.0.7"`) for reproducibility in production pipelines. See [Available images reference](available-images-reference.md) for the full catalogue and per-image guidance.

## Step 2: Create or identify a configuration

List existing configurations to see if one already fits your needs:

```
GET /api/v1/transformations/configurations
```

To create a new configuration, submit a `POST` request with a name, description, and the `data` field containing the image-specific processing specification:

```
POST /api/v1/transformations/configurations
```

```json
{
  "name": "my_study_config",
  "description": "Configuration for study XYZ",
  "data": {
    "source": "csv",
    "destination": "samples"
  }
}
```

The response includes the integer `id` of the created configuration. Record it: you need it in the next step. See [Manage configurations](manage-configurations.md) for full CRUD operations.

## Step 3: Submit a dry-run job

Submit a job with `dry_run` set to `true`:

```
POST /api/v1/transformations/jobs
```

```json
{
  "configuration": {
    "id": <config_id>
  },
  "dry_run": true,
  "image_reference": {
    "name": "<image_name>",
    "version": "latest"
  },
  "input_accessions": ["<attachment_accession>"],
  "volume_size": "30Gi"
}
```

Two optional parameters control resource allocation for the job: `volume_size` and `memory_size`.

The first, `volume_size`, sets the disk space allocated for processing. It must be a Kubernetes resource quantity string, for example, `"4Gi"` for 4 GiB or `"512Mi"` for 512 MiB. The request is rejected if the value is not a valid quantity or is zero. As a guideline: for H5AD input files, allocate at least 1.4× the original file size; for 10x H5 input files, at least 4×; for CSV files, a small value is typically sufficient.

`memory_size` sets the RAM allocated for processing, using the same quantity format, for example, `"512Mi"`. Increase it if a job ends in `FAILED` with `status.reason: OOMKilled` (out-of-memory termination).

For default values for both parameters, see [Available images reference](available-images-reference.md).

By default the job runs against the latest version of the configuration. To pin a specific version (for example, to reproduce an earlier job), add a `version` to the `configuration` object:

```json
"configuration": {
  "id": <config_id>,
  "version": <version>
}
```

The response includes the integer `id` of the created job. Record it for monitoring.

## Step 4: Monitor the job

Poll the job until it reaches a terminal state:

```
GET /api/v1/transformations/jobs/{job_id}
```

Check the `status.state` field in the response. While the job is running, it will be in one of the intermediate states: `PENDING`, `WAITING`, or `RUNNING`. When it finishes, the state will be one of:

`DONE` - the transformation completed successfully.
`FAILED` - the job encountered an error. Check status.reason for a short error code (for example, OOMKilled means the job ran out of memory, so resubmit with a larger memory_size) or review the job logs for the full report.
`CANCELLED` - the job was cancelled manually.

## Step 5: Review the logs

```
POST /api/v1/transformations/jobs/{job_id}/logs
```

Review the log output for:

- Configuration validation messages.
- The file structure report: which metadata keys are present in your input file.
- Linking validation results: whether the transformation output can be linked to existing ODM objects.
- Columns flagged for automatic renaming or data type conversion.

If issues are found, update the configuration using `PUT /api/v1/transformations/configurations/{id}` and repeat from Step 3. See [Manage configurations](manage-configurations.md) for the recommended iteration loop.

## Step 6: Submit the full run

Once the dry run completes without issues, resubmit the job. You can either set `dry_run` to `false` or omit it entirely (it defaults to `false`):

```json
{
  "configuration": {
    "id": <config_id>
  },
  "dry_run": false,
  "image_reference": {
    "name": "<image_name>",
    "version": "latest"
  },
  "input_accessions": ["<attachment_accession>"],
  "volume_size": "30Gi"
}
```

Monitor and review logs the same way as Steps 4–5. When the job completes, the logs contain the ODM accessions of all objects that were created or updated.

## Use-case guides

- For single-cell HDF5 ingestion, see [Single-cell data in ODM: Getting started](single-cell/single-cell-getting-started.md).
- For CSV-to-Sample-group conversion, see the [`metadata-basic` image](available-images-reference.md#metadata-basic).
- For the full endpoint specifications, see [API reference](/swagger/?urls.primaryName=processorsController).
