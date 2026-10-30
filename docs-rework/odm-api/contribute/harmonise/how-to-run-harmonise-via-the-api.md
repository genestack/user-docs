---
diataxis: how-to
tab: odm-api
---

# How to run Harmonise via the API

This guide covers the end-to-end steps of a Harmonise run through the Harmonisation API: check your credentials, start a run, wait until it is ready, ask it for steps, and finish it.

For the concepts behind runs, see [About the Harmonisation API](about-the-harmonisation-api.md). For every field of a run, see the [Harmonisation API reference](harmonisation-api-reference.md).

## Prerequisites

- An API token. See [Authentication and tokens](../../getting-started/authentication-and-tokens.md).
- Curator group membership.
- LLM credentials that ODM can use. See [Manage LLM credentials via the API](manage-llm-credentials-via-the-api.md).

## Step 1: Check your LLM credentials

```text
GET /api/v1/harmonisation/llm-credentials
```

A run can start only if the response's `status` is `USABLE`. A `404 Not Found` response means you have no credentials saved; `PROVIDER_REMOVED` or `MODEL_REMOVED` means you must choose again. In both cases, save your credentials first.

## Step 2: Start a run

```text
POST /api/v1/harmonisation/runs
```

The request has no body. The response, `201 Created`, is the new run:

```json
{
  "id": 42,
  "status": "PENDING",
  "startedBy": "curator@example.com",
  "createdAt": "2026-10-24T17:19:08Z",
  "defaultBucket": "odm",
  "connected": false,
  "steps": []
}
```

Record the `id`: every other call about the run takes it. If you have no usable credentials, the start is refused with `409 Conflict`, and no run is created.

## Step 3: Wait until the run is ready

```text
GET /api/v1/harmonisation/runs/{id}
```

Poll the run until its `status` is `READY`. While it is `PENDING`, its `reason` says what it waits for, for example `Unschedulable` for a moment while its storage is set up, then `ContainerCreating`. A run that stays `PENDING` with a reason such as `ErrImagePull` or `Unschedulable` cannot start: finish it (Step 5), and let your administrator know.

## Step 4: Ask the run for steps

A `READY` or `RUNNING` run takes steps. Each request queues one step after those asked for before and returns it, `201 Created`; the run takes them one at a time. A run that cannot take a step, because it is not ready yet or is already finishing or over, refuses it with `409 Conflict`.

!!! note
    The steps a run can take are early versions and will change as Harmonise develops. See the [Harmonisation API reference](harmonisation-api-reference.md#steps) for the ones available now.

For example, to have the run check your LLM key with the provider:

```text
POST /api/v1/harmonisation/runs/{id}/check-llm
```

```json
{
  "id": "check-llm-1",
  "action": "check-llm",
  "status": "PENDING"
}
```

Poll the run (`GET /api/v1/harmonisation/runs/{id}`) to follow its steps: its `steps` array lists every step you asked for, in order, each with its own `status`. A failed step carries an `error`, and, for a step that called the LLM, a `failure` naming the cause where it is known. A failed step does not end the run.

## Step 5: Finish the run

```text
POST /api/v1/harmonisation/runs/{id}/finish
```

The response, `200 OK`, is the run, now `FINISHING`: the step in progress runs to its end, the steps that have not started are `SKIPPED`, and the run shuts down. Poll the run until its `status` is `FINISHED`, with `finishedAt` and `exitCode` set. A run that was still `PENDING` and never came up is `FINISHED` at once.

There is no cancel: finishing is the only way to end a run. Finishing a run again, or a run that is over, returns it unchanged.

## Step 6: Read your runs later

```text
GET /api/v1/harmonisation/runs
```

Returns every run you started, newest first, those that are over included. Runs in the list carry their steps without the files the steps found; read a single run for the full record. Runs are never deleted.

## Related

- [Run lifecycle](../../../contribute/harmonise/run-lifecycle.md), what each run state means.
- [Manage LLM credentials via the API](manage-llm-credentials-via-the-api.md), the credentials a run needs to start.
- [Harmonisation API reference](harmonisation-api-reference.md), every endpoint, field and value.
