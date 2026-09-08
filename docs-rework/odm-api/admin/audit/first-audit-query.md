---
diataxis: tutorial
tab: odm-api
tickets:
  - ODM-13412
  - ODM-13413
  - ODM-13418
  - ODM-13518
---

# Tutorial: your first audit query

In this tutorial you will retrieve audit events from ODM for the first time, learn to read the anatomy of a single event, and then find the record that your own query left behind. That last step is the point of the exercise: reading the audit log is itself an audited action, and seeing your own footprint appear is the fastest way to understand how the trail fits together.

You will work entirely in the Swagger UI. Nothing you do here changes any data.

## Prerequisites

- The **View Audit Log** permission on your account. Only a user with **Manage organisation** can grant it, and it is never assigned automatically. See [Grant and revoke permissions](../../../admin/manage-users/grant-and-revoke-permissions.md).
- An API token. See [Authentication and tokens](../../getting-started/authentication-and-tokens.md).
- Familiarity with the Swagger UI. See [Swagger orientation](../../getting-started/swagger-orientation.md).

## Step 1: Open the audit definition

1. From the ODM Dashboard, click **API Documentation** to open the Swagger UI.
2. In the definition selector, choose **audit**. This definition contains a single endpoint, `GET /api/v1/audit/events`.
3. Click **Authorize**, select **Genestack API token**, paste your token, and close the dialog.

## Step 2: Retrieve your first events

Expand `GET /api/v1/audit/events`, click **Try it out**, and then click **Execute** without filling in any parameters.

You get back a `200` response containing three things worth looking at.

The `timeRange` object echoes the window that was actually searched. Because you supplied neither `from` nor `to`, ODM defaulted `to` to now and `from` to thirty days before that. Every audit query has a time window, whether or not you asked for one.

The `events` array holds the results, newest first. Results are always ordered by `createTime` descending.

The `cursor` value marks the last event returned, and you will use it in step 6.

## Step 3: Read a single event

Pick any event from the array. Whatever its type, it has the same envelope:

```json
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
```

Read it as a sentence. The `user` block and `clientIp` say who acted. The `type` says what they did. The `createTime` says when, in UTC. The `source` and `sourceType` say where from. The `target` says what was acted on. The `result` says how it went. Only the `details` object varies by event type, and here it names the outgoing and incoming owners of the study.

## Step 4: Find the event your own query created

Your call in step 2 was itself an auditable action, so ODM recorded it.

1. In the `eventType` parameter, select `VIEW_AUDIT_LOG` from the dropdown.
2. Click **Execute**.

The event at the top of the array is almost certainly your own call from step 2. Its `details` object lists the parameters that call used, including the `from` and `to` values ODM defaulted on your behalf, and its `sourceType` is `genestack/auditEvent`.

> **Note:** `VIEW_AUDIT_LOG` events are written in the background rather than synchronously, so if your call does not appear immediately, wait a few seconds and execute again.

Take a note of the `id` inside the `user` block of your own event. That is your user ID, and you need it for the next step.

## Step 5: Narrow by user and time

Now combine two filters to answer a specific question: what has this account done today?

1. Set `userId` to the ID you noted in step 4.
2. Set `from` to today's date at midnight, in the format `yyyy-MM-ddTHH:mm:ss`, for example `2026-08-29T00:00:00`. Leave `to` empty so it defaults to now.
3. Click **Execute**.

The response now contains only your own activity for today. Note that you wrote the datetime without a timezone designator: audit datetimes are always UTC, and an offset such as `+02:00` is rejected with a `400`.

## Step 6: Page through the results

If your instance has been in use for a while, an unfiltered thirty-day query returns more events than one response should carry.

1. Clear the `userId` and `from` parameters.
2. Set `pageLimit` to `5` and click **Execute**. You get five events and a `cursor`.
3. Copy that `cursor` value into the `cursor` parameter and click **Execute** again. You get the next five events, continuing from where the previous page stopped.

Repeat as often as you like. The cursor is an event ID, and paging simply resumes the same ordered result set from that point.

## What you learned

You have queried the audit log, read the common structure that every audit event shares, watched your own access to the log appear in the trail, filtered by acting user and time range, and paged through a large result set.

From here, the [Audit event schema reference](audit-event-schema-reference.md) covers the full parameter set and the errors you are likely to hit, and [How to reconstruct a study's history](reconstruct-a-study-history.md) puts these filters to work on a real investigation.
