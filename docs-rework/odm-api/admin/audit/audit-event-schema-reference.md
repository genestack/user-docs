---
diataxis: reference
tab: odm-api
tickets:
  - ODM-13412
  - ODM-13413
  - ODM-13508
  - ODM-13513
  - ODM-13518
  - ODM-13568
---

# Audit event schema reference

This page describes the parameters `GET /api/v1/audit/events` accepts, the errors it returns, the structure of a successful response, the fields every audit event carries, and the value sets those fields draw on. For what each event type records and the attributes specific to it, see the [Audit event types reference](audit-event-types-reference.md). For parameter types and the full response schema, see the [Swagger UI](/swagger/helper/).

## Query parameters

Every parameter is optional. Called with none, the endpoint returns the last thirty days of events.

| Parameter | Description |
|---|---|
| `from` | Start of the search range, exclusive. Takes a datetime in the format `yyyy-MM-ddTHH:mm:ss`, for example `2026-06-29T14:32:07`, with no timezone designator, and is interpreted as UTC. Defaults to `to` minus thirty days, so setting `to` alone returns the thirty days that preceded it. |
| `to` | End of the search range, inclusive. Same format as `from`. Defaults to the time of the call. |
| `studyAccession` | Genestack study accession. Matches events whose `studyAccession` field is populated, which includes events targeting the study itself and events targeting entities beneath it. |
| `userId` | Integer user ID. Matches the acting user rather than the target, so an `ADD_USER` event is returned under the ID of the administrator who created the account, not the account that was created. |
| `eventType` | A single event type, presented in Swagger as a dropdown. Only one value can be supplied per call, so covering several types means one call per type and combining the results yourself. See the [Audit event types reference](audit-event-types-reference.md). |
| `pageLimit` | Maximum number of events to return, between 0 and 2000 inclusive. |
| `cursor` | Identifier of the event to resume from, taken from the `cursor` value of an earlier response. Keep every other parameter identical between pages. |

## Query errors

| Situation | Response |
|---|---|
| Datetime in the wrong format, or carrying a timezone offset such as `+02:00` | `400`, `Invalid datetime ... for parameter 'from'. Expected format is 'yyyy-MM-ddTHH:mm:ss'` |
| `from` is later than `to` | `Invalid range: 'from' ... must not be after 'to' ...` |
| Study accession does not match the Genestack accession format | `400`, `Invalid study accession: ... does not match Genestack accession format` |
| Study accession is well formed but unknown | Empty `events` array |
| `userId` is not an integer | `400`, `User ID must be integer.` |
| User ID is well formed but unknown | Empty `events` array |
| Cursor value is not a valid identifier | `Invalid cursor value: ...` |
| Cursor is valid but no longer resolves to an event | `Cursor not found: ...` |
| Event type is not one of the supported values | `400`, with a message naming the invalid value |
| Page limit is outside the range 0 to 2000 | The standard page limit error used across ODM endpoints |
| Caller lacks the **View Audit Log** permission | `403`, `Not enough permissions to call method '' of application 'genestack/auditEvent'. Required permissions: [VIEW_AUDIT_LOG]` |

## Response envelope

A response contains the time range that was searched, a cursor for paging, and the matching events ordered by `createTime` descending.

| Key | Description |
|---|---|
| `timeRange.from` | Start of the searched range, exclusive. The default is `to` minus thirty days. |
| `timeRange.to` | End of the searched range, inclusive. The default is the time of the call. |
| `cursor` | Identifier of the last event returned. Supply it as the `cursor` parameter to retrieve the next page. |
| `events` | Array of audit events, newest first |

## Event fields

Every event shares the following envelope. Fields whose value would be null or zero are omitted from the response rather than returned empty.

| Key | Field | Description |
|---|---|---|
| `id` | Event ID | Unique identifier of the audit event. Also used as the paging cursor. |
| `type` | Event type | Name of the action recorded. See the [Audit event types reference](audit-event-types-reference.md). |
| `createTime` | Event creation time | Time of the action in ISO 8601 format, UTC, including milliseconds where available |
| `user.id` | Acting user ID | Integer ID of the user who performed the action |
| `user.displayName` | Acting user name | Name of the user who performed the action |
| `user.email` | Acting user email | Email address of the user who performed the action |
| `clientIp` | Client IP | IPv4 address the action came from |
| `source` | Event source | `UI` or `API` |
| `sourceType` | Event source type | ODM application or API definition that executed the action |
| `studyAccession` | Study accession | Study the event concerns. Omitted when the event has no associated study. |
| `target.dataType` | Target type | Type of the entity the action affected |
| `target.id` | Target ID | Identifier of the entity the action affected |
| `details` | Details | Event-specific attributes. Contents vary by event type. |
| `result.status` | Status | Result of the action |
| `result.statusCode` | Status code | Response code of the action. Omitted when the value would be zero. |
| `result.errorMessage` | Error message | Description of a failure. Omitted when the action did not fail. |

## Example

```json
{
  "timeRange": {
    "from": "2026-05-30T00:00:00Z",
    "to": "2026-06-29T00:00:00Z"
  },
  "cursor": "9f2b1c7a-4e3d-4a91-b2f0-7c6d5e4a1b22",
  "events": [
    {
      "id": "9f2b1c7a-4e3d-4a91-b2f0-7c6d5e4a1b22",
      "type": "CHANGE_OWNER",
      "createTime": "2026-06-28T14:32:07.348Z",
      "user": {
        "id": 182,
        "displayName": "Jane Doe",
        "email": "jane.doe@example.com"
      },
      "clientIp": "10.42.7.118",
      "source": "UI",
      "sourceType": "genestack/study-metainfo-editor",
      "studyAccession": "GSF2006789",
      "target": {
        "dataType": "STUDY",
        "id": "GSF2006789"
      },
      "details": {
        "newUserId": 180,
        "oldUserId": 182,
        "ownershipChangerId": 182
      },
      "result": {
        "status": "SUCCESS",
        "statusCode": 200
      }
    }
  ]
}
```

## Status values

| Value | Meaning |
|---|---|
| `SUCCESS` | The action completed |
| `STARTED` | The action was accepted and is processing asynchronously. Recorded for deletions, with status code `202`. |
| `FAILURE` | The action did not complete. The `errorMessage` field describes why. |

## Target data types

`USER`, `GROUP`, `STUDY`, `SAMPLE_GROUP`, `SAMPLE_OBJECT`, `LIBRARY_GROUP`, `LIBRARY_OBJECT`, `PREPARATION_GROUP`, `PREPARATION_OBJECT`, `CELL_GROUP`, `TABULAR_DATA`, `GENE_VARIANT`, `FLOW_CYTOMETRY`, `REFERENCE_GENOME`, `FILE`, `DICTIONARY`, `TEMPLATE`.

Which of these an event can carry depends on its type. See the [Audit event types reference](audit-event-types-reference.md).

## Source values

The `source` field takes one of two values, `UI` or `API`.

> **Note:** the ODM SDK commands `odm-delete-study`, `odm-share-study`, and `odm-curate-study` record `source: UI`, because they reach the platform through the same invoke mechanism the interface uses. Their `sourceType` still identifies the responsible component.

## Source type values

The `sourceType` field names the ODM application or API definition that executed the action.

| Category | Source types |
|---|---|
| Query and retrieve data | `genestack/integrationUser`, `genestack/studyUser`, `genestack/sampleUser`, `genestack/libraryUser`, `genestack/preparationUser`, `genestack/expressionUser`, `genestack/variantUser`, `genestack/flowCytometryUser`, `genestack/aFileUser`, `genestack/cellUser` |
| Import and curate data | `genestack/integrationCurator`, `genestack/studyCurator`, `genestack/sampleCurator`, `genestack/libraryCurator`, `genestack/preparationCurator`, `genestack/cellCurator`, `genestack/expressionCurator`, `genestack/variantCurator`, `genestack/flowCytometryCurator`, `genestack/aFileCurator`, `genestack/manageData`, `genestack/taskmanager`, `genestack/job` |
| Data sources | `genestack/reference-data`, `genestack/referenceGenome` |
| Organisation management | `genestack/scim-integration`, used for both SCIM users and SCIM groups |
| Processors controller | `genestack/processorsController` |
| Audit | `genestack/auditEvent` |
| Interface applications | `genestack/signin`, `genestack/signout`, `genestack/study-metainfo-editor`, `genestack/usersadmin-api`, `genestack/groupsadmin-api`, `genestack/shareutils`, `genestack/curation`, `genestack/export-data` |

## Related

- [Audit event types reference](audit-event-types-reference.md), what each event type records and its details fields.
- [About audit event recording](about-event-recording.md), attribution and visibility caveats.
