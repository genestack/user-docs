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

ODM supports multiple imports running in parallel. To run concurrent imports, simply submit multiple POST requests, one per entity import. There is no special API configuration needed. As of release 1.58, for example, up to 10 VCF files can be processed simultaneously.
