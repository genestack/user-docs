---
diataxis: how-to
tab: odm-api
tickets:
  - ODM-13417
  - ODM-13509
  - ODM-13513
  - ODM-13552
---

# How to trace data access and exports

Confidentiality obligations, partner agreements, and personal data accountability all turn on the same two questions: who looked at this data, and what left the platform. The audit log answers them with two event types, `EXECUTE_ENTITY_QUERY` for reads and `DOWNLOAD_FILE` for exports and downloads. This guide covers both.

## Prerequisites

- The **View Audit Log** permission and an API token. See [About audit logs](about-audit-logs.md) for the permission and [Authentication and tokens](../../getting-started/authentication-and-tokens.md) for the token.

## Find who viewed a study

Filter by study accession and event type:

```text
GET /api/v1/audit/events?studyAccession=GSF2006789&eventType=EXECUTE_ENTITY_QUERY&from=2026-06-01T00:00:00
```

`EXECUTE_ENTITY_QUERY` means the study was read. The `source` field says how: `UI` for a study opened in the Metadata Editor, or `API` for a study fetched through one of the study definitions, with `sourceType` naming the definition that was called. Not every endpoint in those definitions produces the event, and the [audit event types reference](audit-event-types-reference.md) lists the exceptions. The event has no details section, so beyond that you are working with the acting user, the client IP, and the time.

Two things shape how you read the results.

The event is recorded once per study, not once per request. A search endpoint returning two thousand studies produces two thousand events, so a burst of read events with identical timestamps and the same source type is one query, not two thousand deliberate acts of inspection.

Read event logging can be disabled at instance configuration level because of that volume. If a period you know was busy returns no read events at all, confirm whether logging of this event type is switched off on your instance before concluding that nobody looked at the data.

## Find what left the platform

Filter for downloads the same way:

```text
GET /api/v1/audit/events?studyAccession=GSF2006789&eventType=DOWNLOAD_FILE&from=2026-06-01T00:00:00
```

`DOWNLOAD_FILE` covers four different actions. You tell them apart by the source, the target, and the result, not by the event type:

| Action | How the event appears |
|---|---|
| A whole study exported from the Export Data application | `source: UI`, `dataType: STUDY`, and the study accession as the target ID |
| A single file exported from the same application | `source: UI`, the file's accession as the target ID, and a `dataType` of `FILE` for an attachment or `TABULAR_DATA`, `GENE_VARIANT`, or `FLOW_CYTOMETRY` for omics data |
| An attachment downloaded through `GET /api/v1/as-curator/files/{id}/download` | `source: API`, `dataType: FILE`, and the file's accession as the target ID |
| A PDF previewed from the Data tab of the Metadata Editor | `source: UI`, `dataType: FILE`, and the previewed file's accession as the target ID |

The PDF preview is the row to read carefully. A preview is recorded exactly like a download, so the event proves that the content was displayed to the user, not that a copy was saved. For a confidentiality review, treat it as the file having been read.

In every case `studyAccession` is populated, which is what makes the study-scoped filter above return file-level downloads as well as whole-study exports.

## Build the full access picture

Read and download events tell you who used their access. To establish who held access in the first place, combine them with the sharing history from `CHANGE_ENTITY_ACCESS`, which records each grant and revocation with the group involved and the level of access given. See [How to reconstruct a study's history](reconstruct-a-study-history.md).

The two together answer the question a confidentiality review actually asks: which groups could reach this study during the period, and which of their members did.

## Related

- [Audit event schema reference](audit-event-schema-reference.md), the query parameters, errors, and response structure.
- [How to reconstruct a study's history](reconstruct-a-study-history.md), sharing and ownership history for the same study.
- [About audit event recording](about-event-recording.md), read event volume and the configuration switch.
- [Audit event types reference](audit-event-types-reference.md), the complete event catalogue.
- [Export data](../../../explore/export-data.md), the export workflow these events record.
