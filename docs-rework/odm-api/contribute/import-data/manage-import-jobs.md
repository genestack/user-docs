---
diataxis: how-to
tab: odm-api
---

# How to manage import jobs

This guide explains how to restart failed import jobs and stop running ones. Monitoring and verifying a single import is covered inline in each per-entity import how-to; this page addresses cross-job concerns.

For the full set of job status codes, see the [Job status codes reference](../../reference/job-status-codes-reference.md).

## Restart a failed job

Use `PUT /api/v1/jobs/{jobExecId}/restart` to restart a job that has failed or was stopped before completion.

This is useful when a job failed due to a transient issue (for example, a temporary connectivity problem). Provide the `jobExecId` returned by the original import call.

## Stop a running job

Use `PUT /api/v1/jobs/{jobExecId}/stop` to cancel a job that is currently running.

This is useful when you need to cancel a long-running or stuck job.

## Behaviour by file type

Stop and restart behave differently depending on the entity type being imported:

**Metadata files** (studies, samples, libraries, preparations): stop and restart are fully supported. The job resumes from where it left off after a restart.

**Signal files** (expression, variant, flow cytometry): these are processed very quickly, so stopping and restarting has limited practical use in most cases.

**Attachment files** (documents, images, and other attached files): handled as a single unit. Stop and restart are not applicable.

## Concurrent imports

ODM supports multiple imports running in parallel. To run concurrent imports, simply submit multiple POST requests, one per entity import. There is no special API configuration needed.

The number of imports in progress is capped for the whole ODM instance, not per user:

- By default, at most 5 import jobs run at the same time.
- Further imports wait in a queue of up to 100 jobs by default, and start as running jobs finish. A waiting job has the status `STARTING` until it starts running.
- When the queue is full, ODM rejects a new import with HTTP `503` and the message "Too many imports are in progress: N are running and M are waiting. Please try again later.", where N and M are the two limits above. No job is created, so you can submit the same import again later.

Your instance's administrators set both limits of the import cap, so they may differ from these defaults.

The same cap applies when you restart a job with `PUT /api/v1/jobs/{jobExecId}/restart`. A rejected restart returns the same `503` and leaves the job as it was, so you can restart it again later.

The cap covers the import jobs only. Indexing the contents of signal files into ClickHouse, which Core does once an import has completed, has a limit of its own: by default Core indexes up to 10 variant (VCF), expression or flow cytometry files at once, and the others wait their turn. This is what has let ODM process up to 10 VCF files simultaneously since release 1.58.
