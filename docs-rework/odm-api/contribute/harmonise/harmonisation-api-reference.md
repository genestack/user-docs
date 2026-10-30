---
diataxis: reference
tab: odm-api
---

# Harmonisation API reference

Every endpoint of the Harmonisation API, and the fields and values of what it returns. For the concepts, see [About the Harmonisation API](about-the-harmonisation-api.md). The full specification, where you can also try the calls, is the [Harmonisation API in Swagger](/swagger/?urls.primaryName=harmonisation).

Times are ISO 8601, in UTC.

## Endpoints

| Method and path | Who | Does | Returns |
|---|---|---|---|
| `GET /api/v1/harmonisation/runs` | Curators | Lists the runs you started, newest first, those that are over included | `200`, runs without the files their steps found |
| `POST /api/v1/harmonisation/runs` | Curators | Starts a run with your LLM credentials | `201`, the run |
| `GET /api/v1/harmonisation/runs/{id}` | Curators | Reads a run you started | `200`, the run |
| `POST /api/v1/harmonisation/runs/{id}/steps` | Curators | Queues a `list-files` step | `201`, the step |
| `POST /api/v1/harmonisation/runs/{id}/upload` | Curators | Queues an `upload-to-odm` step | `201`, the step |
| `POST /api/v1/harmonisation/runs/{id}/check-llm` | Curators | Queues a `check-llm` step | `201`, the step |
| `POST /api/v1/harmonisation/runs/{id}/finish` | Curators | Finishes a run | `200`, the run |
| `GET /api/v1/harmonisation/llm-credentials` | Curators | Reads your credentials, without the key | `200`, the credentials |
| `PUT /api/v1/harmonisation/llm-credentials` | Curators | Saves your credentials, replacing any saved before | `200`, the credentials |
| `DELETE /api/v1/harmonisation/llm-credentials` | Curators | Deletes your credentials | `204` |
| `GET /api/v1/harmonisation/llm-providers` | Curators and Harmonisation Administrators | Lists the providers, ordered by name | `200`, providers |
| `POST /api/v1/harmonisation/llm-providers` | Harmonisation Administrators | Adds a provider | `201`, the provider |
| `PUT /api/v1/harmonisation/llm-providers/{id}` | Harmonisation Administrators | Replaces a provider's name, API, base URL and models | `200`, the provider |
| `DELETE /api/v1/harmonisation/llm-providers/{id}` | Harmonisation Administrators | Removes a provider and its models | `204` |

A run's `{id}` is its number. There is no endpoint to delete or cancel a run.

## Errors

| Status | When |
|---|---|
| `400 Bad Request` | A run id that is not a number, or an invalid body: see each endpoint in Swagger. |
| `401 Unauthorized` | No valid token. |
| `403 Forbidden` | Not a Curator, or, to change providers, not a Harmonisation Administrator. |
| `404 Not Found` | No run with this id that you started, no credentials saved, or no provider with this id. |
| `409 Conflict` | Starting a run without usable LLM credentials; a step on a run that cannot take one now, because it is not ready yet or is finishing or over; an upload before any listing found files; adding a provider whose id is in use. |
| `503 Service Unavailable` | The cluster the runs' processing environments run on, or the database that keeps their history, cannot be reached. Retry later. |

## Run

| Field | Description |
|---|---|
| `id` | The run's number: 1, 2, 3, … in the order runs start, across the instance. A start that failed may leave a gap. |
| `status` | One of the [run statuses](#run-statuses). |
| `startedBy` | Email of the Curator who started the run, the only user who sees and steers it. |
| `createdAt` | When the run started. |
| `readyAt` | When the run first became ready to take steps. |
| `finishedAt` | When the run ended; set once it is `FINISHED` or `FAILED`. |
| `exitCode` | Exit code of the run's process; `0` after a clean finish. Absent if it never ran. |
| `reason` | Why the run waits, failed or ended as it did, for example `ErrImagePull` or `Finished before its Pod was ready`. |
| `defaultBucket` | The bucket a `list-files` step lists when it names none. |
| `connected` | Whether the run's processing environment is connected to ODM now; `false` once the run is over. |
| `steps` | The [steps](#steps) you asked for, in order, and `shutdown` last once the run shuts down. |

### Run statuses

| Status | Meaning |
|---|---|
| `PENDING` | The run has started, and its processing environment is being set up. Steps are refused. |
| `READY` | The run waits for a step. |
| `RUNNING` | The run is taking a step. |
| `FINISHING` | The run was finished, and completes the step in progress before it shuts down. |
| `FINISHED` | The run shut down after it was finished. Final. |
| `FAILED` | The run's processing environment stopped, reached its time limit or failed to shut down, or ODM restarted while the run was open. Final. |

See [Run lifecycle](../../../contribute/harmonise/run-lifecycle.md) for how a run moves between them.

## Steps

!!! note
    The step actions other than `shutdown` are early versions and will change as Harmonise develops.

| Field | Description |
|---|---|
| `id` | Unique within the run: `list-files-1`, `upload-to-odm-1`, `check-llm-1`, … and `shutdown`. |
| `action` | `list-files`, `upload-to-odm`, `check-llm` or `shutdown`. |
| `status` | One of the [step statuses](#step-statuses). |
| `startedAt`, `finishedAt` | When the step started and ended. |
| `error` | Why the step failed. |
| `failure` | For a failed step that called the LLM, its [cause](#llm-failures), where the run can tell it. |
| `bucket`, `path` | What a `list-files` step lists, or the listing an `upload-to-odm` step uploads. |
| `files` | What a `list-files` step found: each file's `key`, `size` in bytes and `lastModified`. Absent in run lists. |
| `keys` | The files an `upload-to-odm` step uploads. |
| `upload` | What an `upload-to-odm` step imported into ODM: `studyAccession`, `sampleGroupAccession` and `expressionGroupAccessions`. |

The body of `POST /api/v1/harmonisation/runs/{id}/steps` is optional: `bucket`, the run's `defaultBucket` when absent, and `path`, a folder in the bucket, the whole bucket when absent.

### Step statuses

| Status | Meaning |
|---|---|
| `PENDING` | The step waits for its turn. |
| `RUNNING` | The run is taking the step. |
| `SUCCEEDED` | The step completed. |
| `FAILED` | The step did not complete, also when the run's processing environment failed while the step was sent to it. |
| `SKIPPED` | The step never ran, because the run was finished, or failed, before its turn. |

### LLM failures

| Failure | Cause |
|---|---|
| `LLM_KEY_REJECTED` | The provider refused the key. |
| `LLM_MODEL_UNAVAILABLE` | The provider does not know the model, or the key may not use it. |
| `LLM_UNREACHABLE` | No answer from the provider. |
| `LLM_KEY_MISSING` | The run's Curator had no usable credentials when it started. |

A run keeps the credentials it started with: a key saved since applies to the next run.

## LLM credentials

What `GET` and `PUT /api/v1/harmonisation/llm-credentials` return. ODM never returns the key.

| Field | Description |
|---|---|
| `provider` | Id of the provider. |
| `model` | The model. |
| `status` | `USABLE`: runs can start with them. `PROVIDER_REMOVED` or `MODEL_REMOVED`: a Harmonisation Administrator removed the provider or the model since, and no run can start until you choose again. |
| `updatedAt` | When you last saved them. |

What `PUT` takes:

| Field | Description |
|---|---|
| `provider` | Required. Id of a provider. |
| `model` | Required. One of that provider's models. |
| `apiKey` | Your key: 1 to 1024 printable ASCII characters, without spaces. Required with no credentials saved, or with another provider than the saved one; left out, the saved key stays. |

## LLM provider

| Field | Description |
|---|---|
| `id` | Chosen when the provider is added, and fixed after: lowercase letters, digits and hyphens, at most 64 characters. |
| `name` | The name Curators see, at most 128 characters. |
| `api` | The API runs speak to the provider: `ANTHROPIC`, or `OPENAI`, which also covers endpoints compatible with OpenAI's API. |
| `baseUrl` | The root of the provider's API: `https`, without a version, user info, query or fragment, for example `https://api.anthropic.com`. |
| `models` | At least one model, as the provider names them, in printable ASCII without spaces. Returned sorted. |
| `updatedAt` | Read-only. When the provider was last added or changed. |
