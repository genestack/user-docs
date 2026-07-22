---
diataxis: how-to
tab: odm-api
---

# How to manage user accounts via the API

When you are provisioning users from a script or keeping ODM in step with another system, clicking through the interface one account at a time does not scale. The user-management endpoints let you create accounts, update them, and look up group membership programmatically, so account management can ride along with the rest of your automation.

For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## When to use this

Reach for these endpoints when you are writing automation scripts, synchronising accounts from AD or SCIM, or building system integrations that manage users without a person in the loop. For full SCIM-based provisioning with Active Directory, use the SCIM endpoints instead; see [SCIM integration](../../admin/scim-integration.md).

## Prerequisites

- An API token. See [Authentication and tokens](../getting-started/authentication-and-tokens.md).
- "Manage organisation" permission.

## Look up a user's groups

To retrieve the non-deleted user groups a user belongs to:

```
GET /api/v1/groups
```

You can filter the results by user attributes, for example by `displayName`.

## Create a user

Supply the new user's details in the request body:

```
POST /api/v1/users
```

## Update a user

Supply only the fields you want to change:

```
PATCH /api/v1/users/{id}
```

## Related

- [SCIM integration](../../admin/scim-integration.md), Active Directory / SCIM provisioning.
- [Permissions reference](../../overview/access-control/permissions.md)
- [Authentication and tokens](../getting-started/authentication-and-tokens.md)
