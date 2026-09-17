---
diataxis: how-to
tab: odm-api
tickets:
  - ODM-13412
  - ODM-13508
  - ODM-13568
---

# How to review a user's activity

When you need to establish what a particular account did, the audit log lets you retrieve everything that account was responsible for across the platform. Offboarding checks, security investigations, and compliance requests all come down to the same query. This guide covers the user-scoped investigation.

## Prerequisites

- The **View Audit Log** permission and an API token. See [About audit logs](about-audit-logs.md) for the permission and [Authentication and tokens](../../getting-started/authentication-and-tokens.md) for the token.
- The integer user ID of the account you are investigating.

## Find a user's ID

The audit filter takes an integer user ID rather than an email address. If you only have a name or an address, retrieve a set of events and read the `user` block, which carries all three identifiers:

```json
"user": {
  "id": 182,
  "displayName": "Jane Doe",
  "email": "jane.doe@example.com"
}
```

Filtering by `USER_LOGIN` is usually the fastest way to find the account, since any account that has used ODM produces those events.

## Retrieve the account's activity

Filter by `userId` and bound the time range you care about:

```text
GET /api/v1/audit/events?userId=182&from=2026-06-01T00:00:00&to=2026-06-30T23:59:59
```

The filter matches the acting user, the person who performed the action. It does not match events where the account was the target, which needs the different approach covered below.

## Separate interactive sessions from API activity

`USER_LOGIN` events do not correspond one to one with sign-ins. The event is emitted for API calls as well as for interactive sign-ins through the interface, so an account driving a pipeline can generate hundreds of them in a few minutes.

Use the `source` field to tell them apart. Sign-ins through the interface record `source: UI` with `sourceType: genestack/signin`, while API activity records `source: API` with the source type of the definition that was called, for example `genestack/studyCurator`. Retrieve the account's login events and group them by `source` in your own code.

Apply the same caution to `USER_LOGOUT`. Treat login and logout events as evidence that an account was active, not as a reliable session record.

## Establish what the account did to data

Most of what an account produces is logins and reads. The events that answer the question you were asked are the writes, and they fall into two groups worth reading separately.

The first is what the account made: `CREATE_ENTITY` for studies it created, `CHANGE_ENTITY_METADATA` for metadata versions it published. The second is what the account put beyond its own control: `CHANGE_ENTITY_ACCESS` and `CHANGE_OWNER` for data it opened up or handed over, `DOWNLOAD_FILE` for data it took out, and `DELETE_ENTITY` for data it removed. In an offboarding or security review, start with the second group, because those are the events whose consequences outlive the account.

Where several of these concern the same study, [How to reconstruct a study's history](reconstruct-a-study-history.md) gives you the study-side view of the same events. The [audit event types reference](audit-event-types-reference.md) describes every event type ODM records, with the source, target, and details each one carries.

## Check where the activity came from

Most events carry a `clientIp` field holding the IPv4 address the action came from. A set of events from an unexpected address, or a run of activity from an address that does not match the user's usual pattern, is worth following up. Some events do not carry the field, including sign-out events migrated from the previous audit schema, so its absence on an older event is not itself meaningful.

## Find when an account or group was created

The endpoint has no filter for the event target, so you cannot ask what was done to a particular account. Filter by event type instead and read the targets. In an `ADD_USER` event, the acting user is the administrator who created the account, and `target.id` holds the account they created. Its name and address are in the details:

```json
"details": {
  "displayName": "Jane Doe",
  "email": "jane.doe@example.com"
}
```

Retrieve `ADD_USER` events for the relevant time range and scan for the account you are interested in. The same pattern applies to `CREATE_GROUP`, where `details.groupName` names the group and `target.id` holds its accession.

Creation is as far as this goes. ODM audits the creation of accounts and groups, not later changes to them, so a permission grant or a change of group membership leaves no audit event.

## Related

- [Audit event schema reference](audit-event-schema-reference.md), the query parameters, errors, and response structure.
- [How to reconstruct a study's history](reconstruct-a-study-history.md), the study-scoped view of the same events.
- [About audit event recording](about-event-recording.md), attribution and visibility caveats.
- [Audit event types reference](audit-event-types-reference.md), the complete event catalogue.
