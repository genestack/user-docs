---
diataxis: reference
tab: odm-api
tickets:
  - ODM-13414
  - ODM-13415
  - ODM-13416
  - ODM-13417
  - ODM-13418
  - ODM-13507
  - ODM-13508
  - ODM-13509
  - ODM-13510
  - ODM-13513
  - ODM-13518
  - ODM-13531
  - ODM-13552
  - ODM-13568
---

# Audit event types reference

This page lists every audit event type ODM records, what triggers it, which sources produce it, what it targets, and the event-specific attributes it carries in its `details` object. For the common envelope shared by all events, see the [Audit event schema reference](audit-event-schema-reference.md).

The types are grouped by what they act on: **user accounts**, **user groups**, **data entities**, and **the audit log** itself.

Event types are supplied to the `eventType` query parameter exactly as written here. Only one value can be supplied per call, so covering several types means one call per type and combining the results yourself.

## Summary

<table>
<thead>
<tr><th>Category</th><th>Event type</th><th>Records</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="3">Users</th><td><code>ADD_USER</code></td><td>User account created through the interface or SCIM</td></tr>
<tr><td><code>USER_LOGIN</code></td><td>User signed in, or made an API call</td></tr>
<tr><td><code>USER_LOGOUT</code></td><td>User signed out, or a session expired</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup">Groups</th><td><code>CREATE_GROUP</code></td><td>User group created through the interface or SCIM</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="7">Entities</th><td><code>CREATE_ENTITY</code></td><td>Study created</td></tr>
<tr><td><code>DELETE_ENTITY</code></td><td>Entity deleted</td></tr>
<tr><td><code>CHANGE_ENTITY_ACCESS</code></td><td>Study access granted to or revoked from a group</td></tr>
<tr><td><code>CHANGE_ENTITY_METADATA</code></td><td>New metadata version created by an edit or a restore</td></tr>
<tr><td><code>CHANGE_OWNER</code></td><td>Study ownership transferred</td></tr>
<tr><td><code>EXECUTE_ENTITY_QUERY</code></td><td>Study viewed or returned by a query</td></tr>
<tr><td><code>DOWNLOAD_FILE</code></td><td>Study exported, file downloaded, or PDF previewed</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup">Audit</th><td><code>VIEW_AUDIT_LOG</code></td><td>Audit log retrieved</td></tr>
</tbody>
</table>

## Users

### ADD_USER

A user account is created, either in the Users and Permissions application or through SCIM provisioning.

**Source:** `UI` with source type `genestack/usersadmin-api`, or `API` with source type `genestack/scim-integration`.

**Target:** `USER`, holding the new account's user ID. The acting user is the administrator who created the account.

**Details:**

| Key | Description |
|---|---|
| `displayName` | Name assigned to the new user |
| `email` | Email address of the new user |

### USER_LOGIN

A user signs in through the interface. The event is also emitted for API calls, distinguished by the `source` field, so it is not a count of interactive sessions.

**Source:** `UI` with source type `genestack/signin` for an interactive sign-in, or `API` with the source type of the definition that was called.

**Target:** `USER`, holding the ID of the user who signed in, which matches the acting user.

**Details:** None.

### USER_LOGOUT

A user signs out through the interface, or a session ends on its own. A session the user never signs out of expires 24 hours after it starts, and the expiry records an event of its own, so a logout event does not always mean the user chose to end the session.

**Source:** `UI` with source type `genestack/signout` for a sign-out through the interface.

**Target:** `USER`, holding the ID of the user whose session ended.

**Details:** None.

## Groups

### CREATE_GROUP

A user group is created, either in the Users and Permissions application or through SCIM provisioning.

**Source:** `UI` with source type `genestack/groupsadmin-api`, or `API` with source type `genestack/scim-integration`.

**Target:** `GROUP`, holding the new group's accession.

**Details:**

| Key | Description |
|---|---|
| `groupName` | Name assigned to the new group |

## Entities

### CREATE_ENTITY

A study is created. Studies are currently the only entity type this event covers.

**Source:** `UI` with source type `genestack/study-metainfo-editor` when created through the **Create new study** action, or `API` when created through `POST /api/v1/jobs/import/study`. The ODM SDK also records `API` for study creation.

**Target:** `STUDY`, holding the new study's accession. The `studyAccession` field carries the same value.

**Details:**

| Key | Description |
|---|---|
| `templateAccession` | Accession of the template applied to the study at creation. The default template is recorded when the request names no template. |

### DELETE_ENTITY

An entity is deleted. One event is recorded for each accession supplied, and the result is `STARTED` with status code `202`, because deletion is accepted and then processed asynchronously.

**Source:** `API` with source type `genestack/manageData` when deleted through `DELETE /api/v1/manage-data/data`. The `odm-delete-study` SDK command records `UI`.

**Target:** One of `STUDY`, `SAMPLE_GROUP`, `SAMPLE_OBJECT`, `LIBRARY_GROUP`, `LIBRARY_OBJECT`, `PREPARATION_GROUP`, `PREPARATION_OBJECT`, `CELL_GROUP`, `TABULAR_DATA`, `GENE_VARIANT`, `FLOW_CYTOMETRY`, `REFERENCE_GENOME`, `FILE`, `DICTIONARY`, or `TEMPLATE`. The `studyAccession` field is populated for all of these except `REFERENCE_GENOME`, `DICTIONARY`, and `TEMPLATE`, which are not children of a study.

**Details:**

| Key | Description |
|---|---|
| `objectId` | Internal system identifier of the deleted object, allowing the deletion to be traced in ODM's technical logs |

> **Note:** deletion cascades to child objects, but only the entity named in the request receives an audit event. Child objects removed by the cascade do not produce events of their own.

### CHANGE_ENTITY_ACCESS

Access to a study is granted to or revoked from a user group. One event is recorded per study when several accessions are shared at once.

**Source:** `UI`, both for sharing and revoking through the Metadata Editor or Study Browser and for the `odm-share-study` SDK command, which records source type `genestack/shareutils`. Only the study owner can change access. Revocation is not available through the SDK.

**Target:** `STUDY`.

**Details:**

| Key | Description |
|---|---|
| `action` | `gained` or `lost` |
| `principalType` | `GROUP`. Groups are currently the only supported principal type. |
| `principalId` | Accession of the group that gained or lost access |
| `principalName` | Name of the group that gained or lost access |
| `permission` | `Content View` or `Content Edit` |

### CHANGE_ENTITY_METADATA

A new metadata version is created, either by publishing an edit or by restoring an earlier version.

**Source:** `UI` with source type `genestack/study-metainfo-editor` when published from the Metadata Editor, `API` when created through a curator `PATCH` call, and `UI` with source type `genestack/curation` for the `odm-curate-study` SDK command.

**Target:** `STUDY` or `TABULAR_DATA`. The `studyAccession` field is populated for studies, and for tabular data when the group is linked to a study.

**Details:**

| Key | Description |
|---|---|
| `version` | Identifier of the newly published version |
| `previousVersion` | Identifier of the version it replaced |
| `changeType` | `EDIT` for a published change, `RESTORE` for a revert to an earlier version |
| `restoredFromVersion` | Identifier of the version that was restored. Omitted when `changeType` is `EDIT`. |

> **Note:** this event is emitted where the eventual response is not known, so its status is always `SUCCESS` and it carries no `statusCode` or `errorMessage`. A failed metadata change produces no event.

### CHANGE_OWNER

Ownership of a study is transferred to another user.

**Source:** `UI` with source type `genestack/study-metainfo-editor`.

**Target:** `STUDY`.

**Details:**

| Key | Description |
|---|---|
| `newUserId` | User who received ownership |
| `oldUserId` | User who lost ownership |
| `ownershipChangerId` | User who executed the transfer. Matches the acting user, and is not necessarily the previous owner. |

### EXECUTE_ENTITY_QUERY

A study is viewed or returned by a query. One event is recorded per study, so a query returning two thousand studies produces two thousand events.

**Source:** `UI` when a study is opened in the Metadata Editor, or `API` when a study is returned by the study SPoT and study integration endpoints, in both their user and curator forms. The study versions endpoint, the curator study PATCH endpoint, and the full-text study search endpoints do not produce this event.

**Target:** `STUDY`.

**Details:** None.

> **Note:** logging of this event type can be disabled at instance configuration level through the `genestack.audit.excludedEventTypes` setting.

### DOWNLOAD_FILE

Data leaves the platform, through a study export, a file download, or a PDF preview.

**Source:** `UI` with source type `genestack/export-data` for exports and downloads from the Export Data application, or `API` for an attachment retrieved through `GET /api/v1/as-curator/files/{id}/download`. A PDF preview from the Data tab of the Metadata Editor records `UI`.

**Target:** `STUDY` for a whole study export. For a single file, `FILE` for an attachment or PDF, or `TABULAR_DATA`, `GENE_VARIANT`, or `FLOW_CYTOMETRY` for exported omics data. The `studyAccession` field is populated in all cases.

**Result:** `SUCCESS` with status code `200`.

**Details:** None.

## Audit

### VIEW_AUDIT_LOG

The audit log is retrieved through `GET /api/v1/audit/events`. Every successful call produces one event. The event is written in the background rather than synchronously, so it may take a few seconds to become visible.

**Source:** `API` with source type `genestack/auditEvent`.

**Target:** None.

**Details:** an absent key means the caller did not supply that filter, not that the filter matched nothing.

| Key | Description |
|---|---|
| `from` | Start of the search range used. The default value is recorded when the caller supplied none. |
| `to` | End of the search range used. The default value is recorded when the caller supplied none. |
| `studyAccession` | Study accession the search was filtered by. Recorded only when the caller supplied one. |
| `userId` | Acting user ID the search was filtered by. Recorded only when the caller supplied one. |
| `pageLimit` | Page limit used. The default value is recorded when the caller supplied none. |
| `cursor` | Event ID the page resumed from. Recorded only when the caller supplied one, so it is absent on the first page of a paged sequence and present on every page after it. |
| `resultCount` | Number of events the call returned |

## Related

- [Audit event schema reference](audit-event-schema-reference.md), the query parameters, the common envelope, and the source type catalogue.
- [About audit event recording](about-event-recording.md), attribution and visibility caveats.
