---
sources:
  - path: docs/user-guide/doc-odm-user-guide/about-sc-hdf5-transformations.md
    lines: [54, 77]
  - path: docs/user-guide/doc-odm-user-guide/attachment-transformation.md
    lines: [178, 218]
  - path: docs/user-guide/doc-odm-user-guide/api-reference.md
    lines: [150, 256]
  - path: docs/user-guide/doc-odm-user-guide/transformation-process-reference.md
    lines: [1, 251]
diataxis: explanation
tab: odm-api
tickets:
  - ODM-13233
  - ODM-13239
  - ODM-13304
  - ODM-13324
---

# Transformation job lifecycle

When you submit a transformation job, the Processors Controller provisions the processing environment, tracks the job's state as it runs, and reclaims its compute resources once the job is finished. The Processors Controller does not run the transformation itself. The transformation — the containerized image running inside that environment — does the actual work: it reads its inputs, processes them, writes the resulting objects back into ODM, and uploads its log. This page explains each phase so that you can interpret status responses, reason about failures, and make informed decisions about resource settings.

For the concepts behind transformations, see [About the Processors Controller](about-processors-controller.md). For the full list of job states and the job object's fields, see the [Processors Controller API reference](api-reference.md).

## Submission

Submitting a job is a single API call to `POST /api/v1/transformations/jobs`. The Processors Controller validates your request, registers the job, and returns a numeric job `id`. From this point on, polling `GET /api/v1/transformations/jobs/{id}` tells you the current state of the job.

The configuration you submit can pin a specific version; if you don't, the job runs against the latest version. Either way, the job records the configuration version it ran against, so the audit trail stays intact and the job can be reproduced even if the configuration is updated afterwards.

## Container provisioning

> **[PLACEHOLDER]** The mechanism by which the Processors Controller provisions the container — including the infrastructure layer used, how the container image is pulled and started, and any queue behaviour when multiple jobs are submitted concurrently — is not yet documented here.

Each transformation image is a versioned containerized processing environment. The image name and version you specify in `image_reference` determine which environment is used. The scratch volume defined by `volume_size` is allocated at this stage and is used to store the input file, intermediate files, and output before they are uploaded to ODM. Alongside it, `memory_size` sets how much memory the job is allowed to use; if the transformation exceeds it, the job fails with an out-of-memory error (see [Completion](#completion)). When you don't set these explicitly, their defaults come from the image, falling back to 30Gi of scratch storage and 512Mi of memory if the image doesn't specify them. For sizing guidance, see [Job resource parameters reference](resource-parameters-reference.md).

The job's state, reported as `status.state` when you poll the job, reflects how far this setup has progressed. A newly accepted job starts as `PENDING`: it has been registered, but its processing environment has not started being set up yet — for example, it may be queued, awaiting capacity, or having its scratch storage prepared. Nothing is running at this stage, and the processing container does not exist yet. The job then moves to `WAITING` while the processing environment is being set up, typically as the transformation image is downloaded; the transformation has still not begun running. Once the environment is ready and the transformation starts processing the input, the job is `RUNNING`. From there it ends in one of three terminal states: `DONE` (finished successfully), `FAILED` (finished with an error), or `CANCELLED` (you cancelled it while it was still running — a terminal outcome distinct from failure, carrying no error reason). A further state, `UNKNOWN`, means the job's state cannot currently be determined. For a normal, successful run the order is `PENDING` → `WAITING` → `RUNNING` → `DONE`.

## Execution

While the job stays in the single `RUNNING` state, the transformation works through several internal phases. These are steps within one run, not separate status values — polling the job during any of them returns `RUNNING`. The phases proceed in the following order regardless of image type:

**Configuration loading and validation** — the transformation configuration document is read and all fields are validated. The configuration is checked in two passes. First, its overall structure: if a required top-level setting is missing or malformed, the job can't go any further and stops immediately. If the structure is sound, every individual setting is then checked together, and all problems are reported at once — so you see the full list in one run rather than fixing one error, re-running, and hitting the next.

**Input file retrieval** — the input file accessions you supplied are resolved against ODM and the files are downloaded to the scratch volume. At this stage the pipeline also retrieves the study accession and any metadata needed to determine where the output objects will be linked.

**Processing** — the image-specific transformation logic runs. What it produces depends on the image. For a detailed description of each internal stage for the single-cell HDF5 image, see [Transformation process reference](single-cell/transformation-process-reference.md).

**Output generation** — processed output files are prepared for upload to ODM. In dry-run mode this step is skipped.

## Dry-run mode

When `dry_run: true`, the transformation validates the configuration and input, runs preliminary checks including linking validation, and then exits before generating output or writing any data to ODM. Like any other job, a dry run is retained permanently: its logs stay available through the API afterwards, even though they are not uploaded to ODM as attachments. Use dry runs to iterate on your configuration before committing to a full run; for the steps, see [How to run a transformation](how-to-run-a-transformation.md).

## Completion

When the transformation finishes on its own, the job transitions to either `DONE` or `FAILED`; if you cancel it while it is still running, it transitions to `CANCELLED`. At this point the Processors Controller sets the job's `end_time`, recording the moment the job reached its terminal state; comparing `end_time` against `create_time` gives you the job's total duration.

**On success (`DONE`):** The transformation has written its output objects into ODM and linked them to the appropriate study entities. It also uploads its log to ODM as an attachment on the study that owns the input file. This upload is skipped if `save_logs` is set to `false` in the transformation configuration.

**On failure (`FAILED`):** No ODM objects are written.

<!-- TODO: Confirm whether a mid-run failure can leave partial objects in ODM. If not guaranteed atomic, reword (e.g. "may not have written all, or any, objects"). -->

The job log records the error that caused the failure; retrieve it via `POST /api/v1/transformations/jobs/{id}/logs` to diagnose the problem. A common failure reason is running out of memory: when this happens, the job's status carries the reason `OOMKilled`, meaning the transformation used more memory than `memory_size` allowed. The remedy is to resubmit with a larger `memory_size`.

**On cancellation (`CANCELLED`):** You can cancel a job while it is still running, using `POST /api/v1/transformations/jobs/{id}/cancel`. Cancelling stops the job immediately and records it as `CANCELLED` — a terminal outcome distinct from `FAILED`, carrying no error reason. There is no choice of how the job stops.

**Archival and compute cleanup:**

Finishing and archiving are two separate moments. A job first reaches a terminal state (`DONE`, `FAILED`, or `CANCELLED`); shortly afterwards a background process archives its final status and full logs to permanent storage and frees the job's compute resources — the scratch volume and the processing container. Cancelling a job archives it immediately. Once a job is archived, its `archived` field flips to `true`; you see no other change, because its status and logs keep working exactly as before.

The job record, its final status, and its logs are retained permanently and stay available through the API — they are never auto-deleted, and a job cannot be deleted manually. Archival frees only the compute resources; it does not remove the ODM objects the transformation produced.

## Log availability

A job's logs are retained permanently and are always retrievable, whether the job is still running or long finished.

Via the API, using `POST /api/v1/transformations/jobs/{id}/logs`, the endpoint returns the live logs while the job runs and the archived logs once it has finished — transparently, with no change in how you call it. This applies to successful, failed, and cancelled jobs alike.

Separately, the log is also uploaded to ODM as an attachment on the study that owns the input file as part of the transformation's final steps (unless `save_logs: false` in the configuration), so it sits alongside the job's other generated files.

<!-- TODO: Clarify the relationship between the permanent, API-accessible log archive (new) and the existing behavior of uploading a job's log to ODM as a study attachment. The archive makes API-fetchable logs permanent on its own; whether the study-attachment upload still exists or changes is not yet specified. Do NOT state that a log must be attached to a study to persist. Resolve before publishing. -->
