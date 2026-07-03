# How to manage transformation configurations

This guide shows you how to develop a transformation configuration and iterate on it until it produces the results you want. A configuration is a reusable, versioned JSON document that tells an image how to process your input. The workflow below takes you from a first draft, through dry-run testing, to a validated configuration you can run against your data and reuse across jobs.

For the full field-by-field schema of every configuration endpoint, see the [API reference](#) <!-- TODO(swagger): repoint to OpenAPI/Swagger spec (was api-reference.md#transformation-configurations) -->.

## Prerequisites

- An API token. See [Authentication and tokens](../getting-a-genestack-api-token.md).
- Curator group membership.

## The iteration loop

Developing a configuration is a loop. You create a first draft, submit it as a dry-run job, review the logs, and update the configuration based on the results, repeating until the dry run completes without issues and produces the output you expect. Only then you submit a full run. Once the configuration is working, you can reuse it for any input file with the same structure.

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
  "id": 147,
  "version": 1
}
```

Keep that `id`: you use it to retrieve, update, and reference the configuration in job submissions. For the single-cell HDF5 `hdf5-cells` image, the `data` field follows a different schema. See the [Configuration Reference](single-cell/configuration-reference.md).

## Submit a dry run and review the logs

Submit the configuration as a dry-run job, then read the job logs to see how it behaved against your real input without writing any data. The job-submission and log-retrieval endpoints are covered in [How to run a transformation](how-to-run-a-transformation.md).

## Update and repeat

When the logs show something to fix, update the configuration:

```
PUT /api/v1/transformations/configurations/{id}
```

The request body follows the same structure as the `POST` endpoint. Updating does not overwrite the configuration: the current state is saved as a previous version and the active version is incremented. The same `id` is reused across all iterations, and every earlier version stays retrievable, so you can audit or re-run a job with the exact parameters used in the past.

You cannot update a configuration once it has been archived: `PUT` on an archived configuration returns `409 Conflict`. To change it, create a new configuration instead (see [Archive a configuration](#archive-a-configuration)).

Resubmit the dry-run job against the same configuration and review the logs again. Repeat until the dry run completes without errors or warnings that require action, then submit the full run.

## Review your configurations

At any point you can inspect all available configurations. To list them:

```
GET /api/v1/transformations/configurations
```

The response is a paginated envelope: the configurations are in the `items` array, and `limit`/`offset` query parameters page through the results (default 100 per page). Results are ordered by `id`. By default the list returns only active configurations; to include archived ones as well, set the `include_archived` query parameter to `true` (see [Archive a configuration](#archive-a-configuration)). The list returns the latest version of each configuration, including its full `data`, so you can review the current state of each one without a second request. See [Pagination](#) <!-- TODO(swagger): repoint to OpenAPI/Swagger spec (was api-reference.md#pagination) -->.

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

The versions are returned in the `items` array of a paginated envelope. For the field-by-field schema of these and every other configuration endpoint, see the [API reference](#) <!-- TODO(swagger): repoint to OpenAPI/Swagger spec (was api-reference.md#transformation-configurations) -->.

## Reuse a working configuration

Once you have validated a configuration through dry-run testing, it becomes the foundation of your ingestion pipeline: the same configuration can be applied to any number of input files that share the same structure or come from the same source, without any further setup. This makes it straightforward to automate ingestion, for example, to process a batch of files or integrate transformation jobs into a recurring pipeline.

## Archive a configuration

Configurations are never deleted. When you no longer need one, you archive it:

```
POST /api/v1/transformations/configurations/{id}/archive
```

Archiving applies to the configuration and all of its versions at once. Returns 404 Not Found for an unknown id. If the configuration is already archived, the request returns 409 Conflict with the message: "The configuration {id} is already archived, so it cannot be archived again."

Archiving is a soft retirement, not a deletion:

- **Hidden from the default listing.** `GET /api/v1/transformations/configurations` no longer returns the configuration unless you pass `include_archived=true`.
- **Still retrievable by `id`.** Fetching a configuration or a specific version by its `id` still works, with no filter needed.
- **Still usable in jobs.** You can still submit a job that references an archived configuration.
- **No longer updatable.** `PUT` on an archived configuration returns `409 Conflict`: *"Configuration is archived and cannot be updated. Create a new configuration instead."*

Archiving is one-way: there is no un-archive or delete operation. To resume work from an archived configuration, retrieve it by `id` and create a new configuration from its `data`.
