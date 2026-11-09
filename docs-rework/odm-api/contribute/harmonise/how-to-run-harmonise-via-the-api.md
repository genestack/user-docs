---
diataxis: how-to
tab: odm-api
---

# How to run Harmonise via the API

This guide covers the end-to-end steps of a Harmonise run through the Harmonisation API: check your credentials, start a run, wait until it is ready, ask it for steps, take a study through its phases, and finish it.

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

Poll the run until its `status` is `READY`. While it is `PENDING`, its `reason` says what it waits for, for example `Unschedulable` for a moment while its storage is set up, then `ContainerCreating`. A run that stays `PENDING` with a reason such as `ErrImagePull` or `Unschedulable` cannot start: finish it (Step 6), and let your administrator know.

## Step 4: Ask the run for steps

A `READY` or `RUNNING` run takes steps. Each request queues one step after those asked for before and returns it, `201 Created`; the run takes them one at a time. A run that cannot take a step, because it is not ready yet or is already finishing or over, refuses it with `409 Conflict`.

!!! note
    The phases of a run (Step 5) are not queued like this: see [Step 5](#step-5-take-a-study-through-the-phases). For every step a run can take, see the [Harmonisation API reference](harmonisation-api-reference.md#steps).

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

## Step 5: Take a study through the phases

A run takes a study through three phases, extract, transform and export, each an attempt you review before the next: see [Phases, attempts and review](../../../contribute/harmonise/about-harmonise.md#phases-attempts-and-review). A phase is accepted only when the run is `READY` with no step queued or running; otherwise it is refused with `409 Conflict`. Poll the run until it is `READY` before each request. Transform needs LLM credentials for a provider whose `api` is `OPENAI`. So does feedback on an extraction: with another provider, extract reads the files by their names and ignores the comments.

1. Extract a folder of the bucket. `bucket` defaults to the run's `defaultBucket`:

    ```text
    POST /api/v1/harmonisation/runs/{id}/extract
    ```

    ```json
    {"path": "harmonisation-demo/study-1"}
    ```

    The response, `201 Created`, is the step, `extract-1`. Once it has `SUCCEEDED`, the step carries `reviewKind` `extraction` and `review` `AWAITING`.

2. Read what the attempt extracted:

    ```text
    GET /api/v1/harmonisation/runs/{id}/steps/extract-1/review
    ```

    The response is `{"stepId", "kind", "payload"}`, where `payload` is a JSON object in the format `kind` names. It never changes, so read it once.

3. To request changes, extract again with `feedback` naming the latest successful extract step. The new attempt, `extract-2`, has `revises` `extract-1`, and reads the same bucket and path unless you give others:

    ```json
    {
      "feedback": {
        "attemptStepId": "extract-1",
        "comments": [
          {"context": "object:samples", "comment": "One row per sample, not per file."}
        ]
      }
    }
    ```

    A comment's `context` is free text, such as `file:raw/samples.csv` or `field:Sample.Disease`, or empty for the whole attempt. Once `extract-2` has succeeded, `extract-1` is `superseded`, with `review` `CHANGES_REQUESTED`.

4. To approve the extraction, transform it, naming the template:

    ```text
    POST /api/v1/harmonisation/runs/{id}/transform
    ```

    ```json
    {"templateId": "public_studies"}
    ```

    The step, `transform-1`, has `basedOn` set to the latest successful extract step, which becomes `APPROVED`. Once it has `SUCCEEDED`, read its review (`reviewKind` `transformation`) as in item 2. To request changes, transform again with `feedback` naming the latest successful transform step: the new attempt keeps its extraction and template.

5. To approve the transformation, export it:

    ```text
    POST /api/v1/harmonisation/runs/{id}/export
    ```

    The request has no body. The step, `export-1`, writes the Package to the run's `defaultBucket` under `harmonisation/runs/<run id>/<step id>/`, and imports its study and samples into ODM as you, linked. Once it has `SUCCEEDED`, its `upload` names the `studyAccession`, the `sampleGroupAccession`, the `packageBucket` and the `packageKeys`.

    A failed export can be asked for again. But one that failed part-way may have imported the study, and perhaps the samples, already: its `error` then names them, for example `Import into ODM failed: … (imported before it: study GSF…)`. Check for them in ODM, and delete them, before you export again, or the retry imports a second study.

Once a transform step has succeeded, the run takes no more extract steps, and once an export has succeeded, no more transform steps and no second export (only a successful export counts): such requests are refused with `409 Conflict`. So is a request without `feedback` for a phase that has succeeded already, and `feedback` naming an attempt that is not the latest successful one of its phase. To extract a study again, start a new run.

## Step 6: Finish the run

```text
POST /api/v1/harmonisation/runs/{id}/finish
```

The response, `200 OK`, is the run, now `FINISHING`: the step in progress runs to its end, the steps that have not started are `SKIPPED`, and the run shuts down. Poll the run until its `status` is `FINISHED`, with `finishedAt` and `exitCode` set. A run that was still `PENDING` and never came up is `FINISHED` at once.

There is no cancel: finishing is the only way to end a run. Finishing a run again, or a run that is over, returns it unchanged.

## Step 7: Read your runs later

```text
GET /api/v1/harmonisation/runs
```

Returns every run you started, newest first, those that are over included. Runs in the list carry their steps without the files the steps found and without your feedback; read a single run for the full record. Runs are never deleted.

## Related

- [Run lifecycle](../../../contribute/harmonise/run-lifecycle.md), what each run state means.
- [Manage LLM credentials via the API](manage-llm-credentials-via-the-api.md), the credentials a run needs to start.
- [Harmonisation API reference](harmonisation-api-reference.md), every endpoint, field and value.
