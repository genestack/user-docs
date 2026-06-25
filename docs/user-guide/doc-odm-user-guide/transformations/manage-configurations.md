# How to manage transformation configurations

This guide shows you how to develop a transformation configuration and iterate on it until it produces the results you want. A configuration is a reusable, versioned JSON document that tells an image how to process your input. The workflow below takes you from a first draft, through dry-run testing, to a configuration you can run for real and reuse across jobs.

For the full field-by-field schema of every configuration endpoint, see the [API reference](api-reference.md#transformation-configurations).

## Prerequisites

- An API token. See [Authentication and tokens](../getting-a-genestack-api-token.md).
- Curator group membership.

## The iteration loop

Developing a configuration is a loop. You create a first draft, submit it as a dry-run job, review the logs, and update the configuration to fix whatever the dry run surfaced, repeating until the dry run is clean. Only then do you submit a full run.

```
Create configuration → Submit dry-run job → Review logs
       ↑                                          |
       └──── Update configuration ←──────────────┘
              (if issues found)
```

Each step in the loop maps to an endpoint, covered in the sections below. The dry-run and full-run steps rely on the job-submission workflow described in [How to run a transformation](how-to-run-a-transformation.md).

## Create a first draft

Create a configuration with:

```
POST /api/v1/transformations/configurations
```

The request body requires `data`: the image-specific processing specification. `name` and `description` are optional but recommended, since the list and get responses surface them so you can identify the configuration later.

For the `metadata-basic` image (CSV to Sample group), a minimal request looks like this:

```json
{
  "data": {
    "source": "csv",
    "destination": "samples"
  },
  "description": "Configuration which allows you to transform csv file into Sample group",
  "name": "csv to samples"
}
```

The response is the configuration reference, its server-assigned `id` and the `version` (`1` for a newly created configuration):

```json
{
  "id": 294862386,
  "version": 1
}
```

Keep that `id`: you use it to retrieve, update, and submit jobs against the configuration. For the single-cell HDF5 `hdf5-cells` image, the `data` field follows a different schema. See the [Configuration Reference](single-cell/configuration-reference.md).

## Submit a dry run and review the logs

Submit the configuration as a dry-run job, then read the job logs to see how it behaved against your real input without writing any data. The job-submission and log-retrieval endpoints are covered in [How to run a transformation](how-to-run-a-transformation.md).

## Update and repeat

When the logs show something to fix, update the configuration:

```
PUT /api/v1/transformations/configurations/{id}
```

The request body follows the same structure as the `POST` endpoint. Updating does not overwrite the configuration: the current state is archived as a previous version and the active version is incremented. The same `id` is reused across all iterations, and every earlier version stays retrievable, so you can audit or re-run a job with the exact parameters used in the past.

Resubmit the dry-run job against the same configuration and review the logs again. Repeat until the dry run completes without errors or warnings that require action, then submit the full run.

## Review your configurations

At any point you can inspect what you have. To list your configurations:

```
GET /api/v1/transformations/configurations
```

The response is a paginated envelope: the configurations are in the `items` array, and `limit`/`offset` query parameters page through the results (default 100 per page). The list returns the latest version of each configuration, including its full `data`, so you can review the current state of each one without a second request. See [Pagination](api-reference.md#pagination).

To retrieve a single configuration by its `id`:

```
GET /api/v1/transformations/configurations/{id}
```

This returns the latest version of that configuration as a single object, with the same fields as a list item.

To work with the version history (for example, to compare against or re-run an earlier iteration), list the versions and then retrieve a specific one:

```
GET /api/v1/transformations/configurations/{id}/versions
GET /api/v1/transformations/configurations/{id}/versions/{version}
```

The versions are returned in the `items` array of a paginated envelope. For the field-by-field schema of these and every other configuration endpoint, see the [API reference](api-reference.md#transformation-configurations).

## Reuse a working configuration

Configurations are reusable. Once a configuration is working correctly, you can apply it to multiple input files in subsequent jobs without recreating it.
