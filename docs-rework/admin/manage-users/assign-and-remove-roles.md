---
diataxis: how-to
tab: admin
---

# How to assign and remove roles

This guide explains how to assign or remove roles for a user in ODM.

## Prerequisites

You must have the **Organisation Administrator** role. This role controls access to the Users and Roles application, where all role management takes place.

For a full description of what each role allows, see [Roles](../../overview/access-control/roles.md).

## Steps

1. Click the three-line menu at the top left of the Dashboard.
2. Select **Users and Roles**. A window opens showing all users in the organisation.
3. Use the search bar to find the user you want to update.
4. Tick the checkbox next to a role name to assign that role. Untick it to remove it.

Changes take effect immediately. The user may need to refresh their session before the updated roles are reflected in their UI.

> **Note:** the **Audit Log Administrator** role lets its holder search and review audit events across the platform through the API, where the hover tip reads "Observe audit logs from API". It grants no access to study content, metadata, or files. It is never assigned automatically to any account, and only an **Organisation Administrator** can assign it. See [About audit logs](../../odm-api/admin/audit/about-audit-logs.md).
>
> **Note:** assigning the **Organisation Administrator** role is significant because it allows the recipient to assign roles to other users. Assign it sparingly, and only to users who need to perform admin tasks.

## Related

- [Roles](../../overview/access-control/roles.md)
- [About audit logs](../../odm-api/admin/audit/about-audit-logs.md)
