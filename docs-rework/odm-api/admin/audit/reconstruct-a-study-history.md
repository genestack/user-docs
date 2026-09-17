---
diataxis: how-to
tab: odm-api
tickets:
  - ODM-13414
  - ODM-13415
  - ODM-13416
  - ODM-13507
  - ODM-13510
  - ODM-13531
---

# How to reconstruct a study's history

When a study's metadata looks wrong, its access list is unexpected, or it has disappeared entirely, the audit log lets you rebuild what happened to it and who was responsible. This guide covers the study-scoped investigation: retrieving a study's events, reading its lifecycle in order, and following metadata versions, access changes, and ownership transfers.

## Prerequisites

- The **View Audit Log** permission and an API token. See [About audit logs](about-audit-logs.md) for the permission and [Authentication and tokens](../../getting-started/authentication-and-tokens.md) for the token.
- The Genestack accession of the study you are investigating.

## Retrieve the study's events

Filter by accession, and set `from` far enough back to reach the study's creation. The default window is only thirty days, so an unbounded question needs an explicit start date:

```text
GET /api/v1/audit/events?studyAccession=GSF2006789&from=2025-01-01T00:00:00
```

The response is ordered newest first. For a timeline, read it from the bottom up. If the result set is large, page through it with `pageLimit` and `cursor`, keeping your other filters identical, so you are working from the study's full history. The ordering puts its creation and earliest changes on the last page, which is where a timeline has to begin.

## Read the lifecycle

A study's events tell a consistent story once you know what each type contributes.

`CREATE_ENTITY` is the first record of the study's existence. Its `details.templateAccession` names the template applied at creation, which is often the explanation for an unexpected metadata structure.

`CHANGE_ENTITY_METADATA` records each new metadata version, whether it came from the Metadata Editor, a curator PATCH endpoint, or a curation script.

`CHANGE_ENTITY_ACCESS` records every grant and revocation of access for a group.

`CHANGE_OWNER` records each ownership transfer.

`EXECUTE_ENTITY_QUERY` records views and queries, and `DOWNLOAD_FILE` records exports and downloads. Both are covered in [How to trace data access and exports](trace-data-access-and-exports.md).

`DELETE_ENTITY` records the deletion, and is the last event a study produces.

## Follow the metadata changes

Each `CHANGE_ENTITY_METADATA` event names the metadata version it created and the version it replaced:

```json
"details": {
  "version": "f6c73d63-1d42-40e3-9ecb-4123e1ae530b",
  "previousVersion": "b2419af8-7c05-4e61-9a3d-08f5ce27b914",
  "changeType": "EDIT"
}
```

Chain the events by matching each event's `previousVersion` to the preceding event's `version`. A break in that chain means you have not retrieved the full history, usually because your time range starts too late.

The `changeType` field separates the two ways a version can be created. `EDIT` means someone published a change. `RESTORE` means someone reverted to an earlier version, in which case `restoredFromVersion` names the version they reverted to. The `restoredFromVersion` field is omitted for edits.

Two limits are worth knowing before you draw conclusions. These events tell you that a version was published and by whom, but not which attributes changed, so you still need the version history in the Metadata Editor for the values themselves. See [Manage metadata versions](../../../contribute/version-metadata/manage-metadata-versions.md). These events also always report success, because a failed edit produces no event at all. You will never see a failed metadata change in the log, only a missing one.

## Review access changes

Each `CHANGE_ENTITY_ACCESS` event records one change for one group:

```json
"details": {
  "action": "gained",
  "principalType": "GROUP",
  "principalId": "GSG2000004",
  "principalName": "Curator",
  "permission": "Content View"
}
```

The `action` field is either `gained` or `lost`, which is what lets you rebuild who could see the study at any point in the timeline. The `permission` field distinguishes read access from edit access. `principalType` is always `GROUP`, because groups are currently the only principal type supported for access changes, so a study shared with an individual will always appear as a change to the group that individual belongs to.

Sharing through the interface and through the `odm-share-study` SDK command both produce these events, and both record `source: UI`. Revocation is only possible through the interface.

## Review ownership transfers

Each `CHANGE_OWNER` event names three people, not two:

```json
"details": {
  "newUserId": 180,
  "oldUserId": 182,
  "ownershipChangerId": 182
}
```

`oldUserId` identifies the owner before the transfer and `newUserId` the owner after it. `ownershipChangerId` is whoever executed the transfer, and matches the event's acting user. It is usually the previous owner, but an administrator can transfer a study on someone's behalf, in which case the three IDs are all different. That distinction is the whole reason the field exists, so check it rather than assuming the previous owner initiated the change.

## Investigate a deleted study

A study's accession remains queryable after the study is gone, so the same `studyAccession` filter still returns its full history including the `DELETE_ENTITY` event that ended it.

That event records the deleted object's internal identifier and the status of the removal:

```json
"details": {
  "objectId": 12
},
"result": {
  "status": "STARTED",
  "statusCode": 202
}
```

`status: STARTED` with `statusCode: 202` is proof that someone asked for the study to be deleted, not that the deletion finished. `objectId` is the object's internal system identifier, the value used to trace the removal through ODM's technical logs.

One event is recorded for each entity you asked to delete. Deleting a study also removes its sample, library, preparation, and cell groups, its tabular, variant, and flow cytometry data, and its attached files, but those child objects do not currently produce audit events of their own. If your question is about one of them, the study's `DELETE_ENTITY` event and its `objectId` are the only trail you have.

## Related

- [Audit event schema reference](audit-event-schema-reference.md), the query parameters, errors, and response structure.
- [How to trace data access and exports](trace-data-access-and-exports.md), the view and download side of a study's history.
- [About audit event recording](about-event-recording.md), attribution and visibility caveats.
- [Audit event types reference](audit-event-types-reference.md), the complete event catalogue.
- [About metadata versioning](../../../contribute/version-metadata/about-metadata-versioning.md), how versions are created and restored.
