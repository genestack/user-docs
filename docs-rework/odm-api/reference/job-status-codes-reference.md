---
diataxis: reference
tab: odm-api
---

# Import job status codes reference

Asynchronous import operations return a `jobExecId`. Use this identifier to monitor progress, retrieve results, restart failed jobs, or stop running jobs.

## Endpoints

| Operation | Method | Endpoint |
|---|---|---|
| Get job status and metadata | `GET` | `/api/v1/jobs/{jobExecId}/info` |
| Get final output and accession | `GET` | `/api/v1/jobs/{jobExecId}/output` |
| Restart a failed or stopped job | `PUT` | `/api/v1/jobs/{jobExecId}/restart` |
| Stop a running job | `PUT` | `/api/v1/jobs/{jobExecId}/stop` |

## Status codes

The `status` field in the `/info` response can be one of:

| Status | Meaning |
|---|---|
| `STARTING` | Import job is initialising |
| `RUNNING` | Import job is in progress |
| `STOPPING` | Import job is being stopped |
| `STOPPED` | Import job has been stopped |
| `COMPLETED` | Import job finished successfully |
| `FAILED` | Import job failed with an error |
| `ABANDONED` | Import job was left incomplete, for example by a server restart mid-run |
| `UNKNOWN` | Import job state could not be determined |

## Output response (`/output`)

The `/output` endpoint returns the final result of a completed or failed job:

```json
{
  "status": "COMPLETED",
  "result": {
    "accession": "GSF1283528"
  }
}
```

For group-level imports, the result object uses `groupAccession` instead of `accession`.

## Behaviour by file type

The behaviour of stop and restart actions depends on the type of file being processed:

| File type | Stop/restart behaviour |
|---|---|
| Metadata files (studies, samples, libraries, preparations) | Stop and restart are supported. The job resumes from where it left off. |
| Signal files (expression, flow cytometry, variant) | Processed quickly; stop and restart have limited practical use. |
| Attachment files | Handled as a single unit; stop and restart are not applicable. |

## Related

- [Manage import jobs](../contribute/import-data/manage-import-jobs.md)
- Per-entity import how-tos: [Import study metadata](../contribute/import-data/import-study-metadata.md), [Import sample metadata](../contribute/import-data/import-sample-metadata.md), and others in the same section.
