---
diataxis: how-to
tab: admin
---

# How to assign and remove roles

This guide explains how to assign or remove roles in ODM. The Users and Roles application has two tabs for this. On the **Users** tab you change the roles of one user. On the **Roles** tab you change who holds one role.

## Prerequisites

You must have the **Organisation Administrator** role. This role controls access to the Users and Roles application, where all role management takes place.

For a full description of what each role allows, see [Roles](../../overview/access-control/roles.md).

## Change the roles of a user

1. Click the three-line menu at the top left of the Dashboard.
2. Select **Users and Roles**. The **Users** tab opens, listing all users in the organisation with their roles.
3. Use the **Name or email** search field to find the user you want to update.
4. Click the user's row, or its edit button. A panel opens on the right with the user's details and the roles, grouped into four categories: **Administration**, **Configuration**, **Data stewardship** and **Compliance**. Each role shows a short description of what it allows.
5. Tick the checkbox next to a role to assign it. Untick it to remove it.

ODM saves each change as soon as you toggle the checkbox, and the role chips in the user's row update with it. To close the panel, click the × button or click the user's row again.

## Add users to a role or remove them from it

1. Click the three-line menu at the top left of the Dashboard.
2. Select **Users and Roles**, then open the **Roles** tab. The roles are listed on the left with the number of users who hold each one.
3. Select the role. Its description and its members are shown on the right.
4. To add users, click the **Add users to this role** field and select one or more users in the list. Type a name or email to narrow it down. The list shows users who cannot be added under **Can't be added**, each with the reason: **Already a member** or **Deactivated**.
5. Click **Add 1 user** (or **Add N users**). The users appear under **Members** straight away.
6. To remove a user from the role, click **Remove** next to their name in the **Members** list.

Click a member's name to open their roles on the **Users** tab. Both tabs show the same data, so a change on one appears on the other without a reload.

Changes take effect immediately, but the user may need to refresh their session before their UI shows the updated roles.

> **Note:** you cannot remove the **Organisation Administrator** role from yourself. In your own panel its checkbox is disabled, and on the **Roles** tab you cannot click **Remove** next to your own name. Another Organisation Administrator can remove it for you.
>
> **Note:** the **Audit Log Administrator** role lets its holder search and review audit events across the platform through the API. It grants no access to study content, metadata, or files. It is never assigned automatically to any account, and only an **Organisation Administrator** can assign it. See [About audit logs](../../odm-api/admin/audit/about-audit-logs.md).
>
> **Note:** assigning the **Organisation Administrator** role is significant because it allows the recipient to assign roles to other users. Assign it sparingly, and only to users who need to perform admin tasks.

## Related

- [Roles](../../overview/access-control/roles.md)
- [About audit logs](../../odm-api/admin/audit/about-audit-logs.md)
