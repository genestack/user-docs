---
diataxis: explanation
tab: odm-api
---

# Transformation job lifecycle

When you submit a transformation job, the Processors Controller provisions the processing environment, tracks the job's state as it runs, and reclaims its compute resources once the job is finished. The Processors Controller does not run the transformation itself. The transformation (the containerized image running inside that environment) does the actual work: it reads its inputs, processes them, and writes the resulting objects back into ODM. This page explains each phase so that you can interpret status responses, reason about failures, and make informed decisions about resource settings.

For the concepts behind transformations, see [About the Processors Controller](about-processors-controller.md). For the full list of job states and the job object's fields, see the [Processors Controller API reference](/swagger/?urls.primaryName=processorsController).

## Submission

Submitting a job is a single API call to `POST /api/v1/transformations/jobs`. The Processors Controller validates your request, registers the job, and returns a numeric job `id`. From this point on, polling `GET /api/v1/transformations/jobs/{id}` tells you the current state of the job.

Both configuration reference and image reference accept an optional version parameter. If you specify a version, that exact version is used. If you specify "latest" or omit the version entirely, the most recent version is used. Either way, the job records the exact configuration version and image version it ran against, so any past job can be audited or reproduced exactly, even if either has been updated since.

## Container provisioning

Each transformation image is a versioned containerized processing environment. The image name and version you specify in `image_reference` determine which environment is used. The scratch volume defined by `volume_size` is allocated at this stage and is used to store the input file, intermediate files, and output before they are uploaded to ODM. Alongside it, `memory_size` sets how much memory the job is allowed to use; if the transformation exceeds it, the job fails with an out-of-memory error (see [Completion](#completion)). 
The job's state, reported as `status.state` when you poll the job, reflects how far this setup has progressed. A newly accepted job starts as `PENDING`: it has been registered, but its processing environment has not started being set up yet: for example, it may be queued, awaiting capacity, or having its scratch storage prepared. Nothing is running at this stage, and the processing container does not exist yet. The job then moves to `WAITING` while the processing environment is being set up, typically as the transformation image is downloaded; the transformation has still not begun running. Once the environment is ready and the transformation starts processing the input, the job is `RUNNING`. From there it ends in one of three terminal states: `DONE` (finished successfully), `FAILED` (finished with an error), or `CANCELLED` (you cancelled it while it was still running, a terminal outcome distinct from failure, carrying no error reason). For a normal, successful run the order is `PENDING` → `WAITING` → `RUNNING` → `DONE`.

A job whose requested memory or volume size exceeds the available resources is terminated after a scheduling timeout and reported as `FAILED` with the reason `Unschedulable`.

## Execution

While the job stays in the single `RUNNING` state, the transformation works through several internal phases. These are steps within one run, not separate status values: polling the job during any of them returns `RUNNING`. The phases proceed in the following order regardless of image type:

**Configuration loading and validation:** the transformation configuration document is read and all fields are validated. The configuration is checked in two passes. First, its overall structure: if a required top-level setting is missing or malformed, the job can't go any further and stops immediately. If the structure is sound, every individual setting is then checked together, and all problems are reported at once, so you see the full list in one run rather than fixing one error, re-running, and hitting the next.

**Input file retrieval:** the input file accessions you supplied are resolved against ODM and the files are downloaded to the scratch volume. At this stage the pipeline also retrieves the study accession and any metadata needed to determine where the output objects will be linked.

**Processing:** the image-specific transformation logic runs. What it produces depends on the image. For a detailed description of each internal stage for the single-cell HDF5 image, see [Transformation process reference](single-cell/transformation-process-reference.md).

**Output generation:** processed output files are prepared for upload to ODM. In dry-run mode this step is skipped.

**Output loading and linking:** the transformation calls ODM's APIs to create or update ODM entities with the generated output files. The job is considered completed when all import and linking operations finish successfully. If the job fails at this stage, some objects may have already been written to ODM and will need to be deleted manually.

Once the job reaches DONE, ODM begins internal indexing of the imported data - this is not part of the transformation job, but the transformed data may not be immediately available for querying until indexing completes.

## Dry-run mode

When `dry_run: true`, the transformation validates the configuration and input, runs preliminary checks including linking validation, and then exits before generating output or writing any data to ODM. Like any other job, a dry run is retained permanently: its logs stay available through the API. Use dry runs to iterate on your configuration before committing to a full run; for the steps, see [How to run a transformation](how-to-run-a-transformation.md).

## Completion

When the transformation finishes on its own, the job transitions to either `DONE` or `FAILED`; if you cancel it while it is still running, it transitions to `CANCELLED`. At this point the Processors Controller sets the job's `end_time`, recording the moment the job reached its terminal state; comparing `end_time` against `create_time` gives you the job's total duration.

**On success (`DONE`):** The transformation has written its output objects into ODM and linked them to the appropriate study entities.

**On failure (`FAILED`):** Whether any ODM objects were written depends on how far the job got. A failure during the earlier phases (configuration validation, input retrieval, or processing) writes nothing to ODM. Output objects are created and linked in the final phase sequentially, so a failure there can leave some objects already written to ODM while later ones were never created. Any objects written before the failure remain in ODM and must be deleted manually.

The job log records the error that caused the failure; retrieve it via `POST /api/v1/transformations/jobs/{id}/logs` to diagnose the problem. Failures come in two kinds: infrastructural failures, which relate to the processing environment, and image-specific failures, which come from the transformation itself. Both kinds are recorded in the job log, so review it to find the specific problem before resubmitting.

**On cancellation (`CANCELLED`):** You can cancel a job while it is still running, using `POST /api/v1/transformations/jobs/{id}/cancel`. Cancelling stops the job immediately and records it as `CANCELLED`, a terminal outcome distinct from `FAILED`, carrying no error reason. Cancellation cannot be undone; to retry, submit a new job with the same parameters.

**Archival and compute cleanup:**

Finishing and archiving are two separate moments. A job first reaches a terminal state (`DONE`, `FAILED`, or `CANCELLED`); shortly afterwards a background process archives its final status and full logs to permanent storage and frees the job's compute resources: the scratch volume and the processing container. Cancelling a job archives it immediately. Archiving is automatic: there is no manual archive or un-archive action. Once a job is archived, its response reports `archived: true`. Archiving changes nothing else about how you work with the job: its status and logs keep working exactly as before.

Archiving does change one thing: the jobs listing. By default, `GET /api/v1/transformations/jobs` returns only active jobs, keeping historical entries out of your working view. To include archived jobs as well, pass `include_archived=true`. Retrieving a single job by its `id` (`GET /api/v1/transformations/jobs/{id}`) and fetching its logs (`POST /api/v1/transformations/jobs/{id}/logs`) work regardless of archive status. An archived job can no longer be cancelled, as it has already finished.

The job record, its final status, and its logs are retained permanently and stay available through the API: they are never auto-deleted, and a job cannot be deleted manually. Archival frees only the compute resources; it does not remove the ODM objects the transformation produced.

## Log availability

A job's logs are retained permanently and are always retrievable, whether the job is still running or long finished.

Via the API, using `POST /api/v1/transformations/jobs/{id}/logs`, the endpoint returns the live logs while the job runs and the archived logs once it has finished, transparently, with no change in how you call it. This applies to successful, failed, and cancelled jobs alike.
