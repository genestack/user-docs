---
diataxis: explanation
tab: odm-api
tickets:
  - ODM-13412
  - ODM-13413
  - ODM-13418
---

# About audit logs

Life sciences organisations hold some of their most valuable and most regulated assets in a data management platform: clinical and omics studies, curated metadata, and files shared across teams and external partners. Sooner or later, someone asks the same question about one of them. Who changed this, and when?

ODM's audit log answers that question. Every significant action against a user, a group, or a study is recorded as a structured audit event, and those events are retrieved through a dedicated REST endpoint protected by its own permission. The result is a trail designed for human review rather than a technical log that happens to contain the answer somewhere.

## Why the audit log exists

Regulations and guidelines governing electronic records in the life sciences, including FDA 21 CFR Part 11 and EU GMP Annex 11, expect systems to maintain secure, computer-generated audit trails that record who performed an action and when. The audit log gives you that trail, so you can produce it directly when required.

It also supports day-to-day accountability. When metadata is edited, a study is deleted, or ownership is transferred, someone eventually asks who did it. Without a trail, there is no way to answer, and no way to tell a simple mistake apart from a process failure or from misuse.

Security investigation depends on the same records. Unusual sign-in activity, unexpected exports, or access granted to the wrong group are hard to notice if nothing records logins, downloads, and sharing changes. When an incident is suspected, the audit log is what an investigator reconstructs the timeline from.

Data integrity principles, often summarised as ALCOA+, require that records be attributable and that their history be traceable. If a metadata value looks wrong, you need to see when it changed, which version preceded it, and whether an earlier version was restored. Audit events for metadata changes carry the version identifiers that make that history followable.

Finally, collaborative work spreads data around. Studies are shared with internal groups and external partners, and files leave the platform through exports. Recording sharing changes and downloads is what lets you answer which groups could reach a study during a given period and who acted on it, questions that matter for confidentiality obligations, partner agreements, and personal data accountability under GDPR.

## What the log covers

Audit events cover the lifecycle of users, groups, and data entities. On the user and group side, that means account creation, sign-in, sign-out, and group creation. On the data side, it means study creation, metadata changes, sharing and revocation, ownership transfer, viewing and querying, export and download, and deletion. Reading the audit log is itself recorded, as described below.

Every event answers who, what, when, where from, and with what result. Each one carries the acting user's identity and client IP address, the event type, the target entity's type and identifier, event-specific details such as the previous and new metadata version identifiers, the creation time in UTC, whether the action came from the interface or the API, which application or API definition executed it, and the outcome. For the complete list of event types and what triggers each one, see the [Audit event types reference](audit-event-types-reference.md). For the field structure, see the [Audit event schema reference](audit-event-schema-reference.md).

## Who can read the audit log

Reading audit events requires the **View Audit Log** permission, which allows the holder to search and review audit events across the platform for investigation, compliance, and support purposes.

The permission is narrow. It grants no data access of its own: a holder can see that a study was created, shared, or deleted, and by whom, but cannot open study content, metadata, or files, and cannot perform any action on a study unless they also hold access to it through the normal sharing model. Neither **Access all data** nor **Manage organisation** confers the ability to retrieve audit events on its own.

It is also never granted automatically. Only a user with the **Manage organisation** permission can assign it, and no account receives it by default. For the permission table and how it sits alongside the others, see [Permissions](../../../overview/access-control/permissions.md). For the assignment workflow in the interface, see [Grant and revoke permissions](../../../admin/manage-users/grant-and-revoke-permissions.md).

Calling the endpoint without the permission returns `403` with a message naming the required permission:

```text
Not enough permissions to call method '' of application 'genestack/auditEvent'. Required permissions: [VIEW_AUDIT_LOG]
```

## Reading the log is itself audited

Access to an audit trail is itself sensitive, so every successful call to the audit endpoint generates a `VIEW_AUDIT_LOG` event recording who queried the log, when, and which range they searched. Anyone reviewing the platform's history can therefore see not only what was done to the data but also who has been looking at the record of it.

## Access is through the API

The audit log has no interface of its own. Events are retrieved from `GET /api/v1/audit/events`, documented in Swagger under the `audit` definition, which makes the trail straightforward to pull into an external compliance system, a scheduled report, or an investigation script. The endpoint returns JSON and filters on four things: time range, study, acting user, and event type.

No other field can be used as a filter. Every field is present in the returned events, either in the envelope every event shares or in the event-specific `details`, so you narrow the results in your own code after retrieving them.

See [Tutorial: your first audit query](first-audit-query.md) to start using the endpoint, the [Audit event schema reference](audit-event-schema-reference.md) for its parameters and errors, and the [Swagger UI](/swagger/helper/) for the specification.

## Related

- [About audit event recording](about-event-recording.md), how events are attributed, when they become visible, and what the log does not tell you.
- [Tutorial: your first audit query](first-audit-query.md), a guided first pass through the endpoint.
- [Audit event schema reference](audit-event-schema-reference.md), the query parameters, errors, and event field structure.
- [Audit event types reference](audit-event-types-reference.md), the complete event catalogue.
- [Permissions](../../../overview/access-control/permissions.md), how **View Audit Log** relates to the other platform permissions.
