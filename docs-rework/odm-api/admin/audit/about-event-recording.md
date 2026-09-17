---
diataxis: explanation
tab: odm-api
tickets:
  - ODM-13410
  - ODM-13414
  - ODM-13417
  - ODM-13508
  - ODM-13509
  - ODM-13510
---

# About audit event recording

An audit trail is only as useful as your confidence in it. Before you draw conclusions from a set of events, it helps to know how each one was attributed, how soon after the action it became visible, and which actions leave no trace at all. This page covers all three.

## Where an event says it came from

Every event records two things about its origin. The `source` field says whether the action came from the interface or the API, and takes the value `UI` or `API`. The `sourceType` field names the specific ODM application or API definition that executed it, for example `genestack/study-metainfo-editor` for an action taken in the Metadata Editor or `genestack/manageData` for a deletion issued against the manage-data endpoint. The full set of values is listed in the [Audit event schema reference](audit-event-schema-reference.md).

Note that `source` tells you which channel an action arrived through, not whether a person or a script performed it. Several ODM SDK commands reach the platform through the same invoke mechanism the interface uses, so they are recorded as `source: UI`. Read `sourceType` when you need to know what actually executed an action: it names the responsible component in every case. The [Audit event types reference](audit-event-types-reference.md) gives the values each event type carries.

## When an event becomes visible

Events fall into two groups, and the difference matters when you query the log immediately after an action.

Governance actions are written synchronously. `CREATE_ENTITY`, `CHANGE_ENTITY_ACCESS`, `CHANGE_OWNER`, and `DELETE_ENTITY` are committed to the audit store before the originating API call returns, which makes them durable at the moment the caller sees a response and queryable immediately afterwards. They are also written only after the action itself has taken effect, so an action that failed and was rolled back leaves no audit event behind.

Everything else is batched and written in the background. Sign-ins, metadata changes, read events, downloads, and audit log views may take a few seconds to appear. If you query for an event you have just triggered and do not find it, waiting briefly and querying again is usually all that is needed.

## Ordering and time

Events are stored and returned in UTC, and the `from` and `to` parameters are interpreted as UTC regardless of your local timezone. This keeps events from different users directly comparable, but it also means a range written in local time selects the wrong window. Convert before you query. The [Audit event schema reference](audit-event-schema-reference.md) gives the accepted format.

Results are ordered by `createTime` descending, so the newest event comes first. This is the only ordering the endpoint returns, and there is no parameter to change it. To follow a sequence of events chronologically, read the results from the bottom up. That order holds even for actions that fall within the same second, because `createTime` carries milliseconds where they are available.

## Read events and their volume

`EXECUTE_ENTITY_QUERY` records one event per study rather than one per request, so a request returning two thousand studies produces two thousand events, each carrying the accession of the study it concerns. This is what allows the `studyAccession` filter to return every view of a study, whatever request produced it. A confidentiality review or a security investigation can therefore scope to a single study. It also means a block of read events sharing a timestamp and a source type is one query rather than two thousand separate inspections.

The cost is volume, because read events dominate the log on an active instance. For that reason, logging of this event type can be switched off at instance configuration level through the `genestack.audit.excludedEventTypes` setting, which currently covers read events alone. If a period you know was busy returns no `EXECUTE_ENTITY_QUERY` events at all, check whether the event type is excluded on your instance before concluding that nobody looked at the data.

## What the audit log does not tell you

A few behaviours will mislead you if you are not expecting them.

`USER_LOGIN` is not a count of interactive sign-ins. The event is emitted for API calls as well as for sign-ins through the interface, distinguished by the `source` field. A script making several hundred API calls generates several hundred `USER_LOGIN` events with `source: API`. Filter on `source` before treating login events as session activity.

Deletion is recorded at the level of the entity you asked to delete, not at the level of everything that went with it. Deleting a study produces a single `DELETE_ENTITY` event for the study, even though the deletion cascades through its sample, library, preparation, cell, tabular, variant, and flow cytometry groups and its attached files. Those child objects do not currently receive their own events. The `objectId` recorded in the event's details is the internal system identifier, which allows the full extent of the deletion to be traced in ODM's technical logs.

`CHANGE_ENTITY_METADATA` is written at the moment the new version is created, so it always reports `SUCCESS` and carries no `statusCode` or `errorMessage`. A failed edit produces no event at all, so a missing event is the only signal that a change did not go through. `statusCode` is omitted from any event whose originating operation returns no response code, which is not a sign of failure.

Events that predate the current audit schema were migrated into it, and a few fields could not be reconstructed. Older sign-out events may lack a client IP, and older API sign-ins may lack a source type. Recent events are unaffected.

## Related

- [About audit logs](about-audit-logs.md), what the audit log is for and who can read it.
- [Audit event types reference](audit-event-types-reference.md), what triggers each event type.
- [Audit event schema reference](audit-event-schema-reference.md), query parameters, field structure, and source type values.
