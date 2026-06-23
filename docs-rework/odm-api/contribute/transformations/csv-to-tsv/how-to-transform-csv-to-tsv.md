---
sources:
  - path: docs/user-guide/doc-odm-user-guide/attachment-transformation.md
    lines: [14, 218]
diataxis: how-to
tab: odm-api
task: task-110
tickets:
  - ODM-13233
---

# How to transform a CSV file to a Sample group

This guide explains how to convert a CSV file attached to a study into an ODM-indexable Sample metadata group using the `metadata-basic` transformation image.

ODM accepts TSV files as a source of metadata but cannot directly ingest CSV files. The `metadata-basic` transformation converts CSV to TSV and automatically imports the result as a Sample group in the same study.

For the general transformation concepts (configurations, images, jobs), see [About the Processors Controller](../about-processors-controller.md).

## Prerequisites

- An API token and Curator group membership. See [Authentication and tokens](../../../getting-started/authentication-and-tokens.md).
- A CSV file uploaded as an attachment to your study. See [Import attached files](../../import-data/import-attached-files.md).
- The attachment's ODM accession.

## Step 1: Identify the metadata-basic image and version

List available transformation images:

```
GET /api/v1/transformations/images
```

Look for entries with `name: "metadata-basic"`. Note the version you want to use (for example, `"latest"`); take the exact version string from the response above. See [Available images reference](../available-images-reference.md) for the full catalogue.

## Step 2: Create a configuration

Create a configuration that tells the transformation where to place the converted data:

```
POST /api/v1/transformations/configurations
```

```json
{
  "data": {
    "source": { "csv": {} },
    "destination": { "samples": {} }
  },
  "description": "Configuration which allows you to transform csv file into Sample group",
  "name": "csv to samples"
}
```

Record the `id` from the response. You can reuse this configuration for other CSV files with the same structure. See [Manage configurations](../manage-configurations.md).

## Step 3: Submit the transformation job

```
POST /api/v1/transformations/jobs
```

```json
{
  "input_accessions": ["<ATTACHMENT_ACCESSION>"],
  "configuration_reference": { "id": <CONFIG_ID> },
  "image_reference": {
    "name": "metadata-basic",
    "version": "latest"
  },
  "dry_run": false
}
```

`volume_size` is omitted because the `metadata-basic` image declares a `5Gi` default that is ample for CSV files. If you want it explicit, add `"volume_size": "5Gi"` (a string with a unit suffix) — never a bare integer.

By default the job runs against the latest version of the configuration; add a `version` to the `configuration_reference` object to pin an earlier one.

> **[Subject to change — ODM-13233]** The exact name and shape of the `configuration_reference` field are not yet finalized. Verify against the released API before relying on it.

The response contains the integer `id` of the created job.

## Step 4: Monitor the job

Poll until the job reaches a terminal state:

```
GET /api/v1/transformations/jobs/{id}
```

The `status.state` field may first report `PENDING` or `WAITING`, then transitions through `RUNNING` before reaching `DONE` or `FAILED`.

## Step 5: Inspect the result

The transformation converts the CSV to TSV and automatically triggers the multipart sample import endpoint. A new Sample metadata group is created in ODM in the same study where the attachment was placed.

To retrieve the transformation logs:

```
POST /api/v1/transformations/jobs/{id}/logs
```

> Logs remain available after the job finishes; they are archived to long-term storage and served from there once the job's Pod is removed.

## Related

- [About the Processors Controller](../about-processors-controller.md)
- [Available images reference](../available-images-reference.md)
- [Manage configurations](../manage-configurations.md)
- [How to run a transformation](../how-to-run-a-transformation.md)
- [Multipart uploads reference](../../import-data/multipart-uploads-reference.md)
