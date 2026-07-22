---
diataxis: reference
tab: overview
---

# Permissions

Once a user is created, permissions can be assigned in the **Users and Permissions** section by any user who holds the **Manage organisation** permission. The system superuser account `root@genestack.com` is created by default with full management rights. Hovering over each permission in the UI displays a tooltip with its capabilities.

| Permission | Actions | Recommendation |
|---|---|---|
| Manage organisation | Manage permissions; manage study ownership; create and deactivate users; change user passwords | Powerful system-level permission. Grant only to a few trusted administrators. |
| Set up templates | Create new templates; alter existing templates | Changes affect all users. Assign only to responsible Data Owners. |
| Configure facets | Set the desired list and order of facets in the Study Browser | Changes affect all users. Assign only to responsible Data Owners. |
| Manage groups | Access and manage all groups, even without admin or membership rights | Use primarily for integration purposes. |
| Access all data | Access all studies in the system, even if not shared | Use only for integration or administrative purposes. |

For the workflow to grant or revoke permissions, see [Grant and revoke permissions](../../admin/manage-users/grant-and-revoke-permissions.md). For how permissions interact with groups, see [Groups and roles](groups-and-roles.md).
