---
diataxis: reference
tab: overview
---

# Roles

Once a user is created, roles can be assigned in the **Users and Roles** application by any user who holds the **Organisation Administrator** role. The system superuser account `root@genestack.com` is created by default with full management rights. Hovering over each role in the UI displays a tooltip with its capabilities.

These are platform roles, assigned to individual users across the whole instance. They are separate from group roles (group member and group admin), which apply within a single group; see [Groups](groups.md).

| Role | Actions | Recommendation |
|---|---|---|
| Organisation Administrator | Manage roles; create and deactivate users; change user passwords | Powerful system-level role. Assign only to a few trusted administrators. |
| Template Administrator | Create new templates; alter existing templates; delete templates through the API or the ODM SDK | Changes affect all users. Assign only to responsible Data Owners. |
| Catalogue Administrator | Set the desired list and order of facets in the Study Browser | Changes affect all users. Assign only to responsible Data Owners. |
| Group Administrator | Access and manage all groups, even without admin or membership rights | Use primarily for integration purposes. |
| Access all data | Access all studies in the system, even if not shared | Use only for integration or administrative purposes. |
| Ownership Recovery Administrator | List studies whose owner is deactivated; assign them a new owner through the API | Reassigns studies regardless of sharing. Assign only to administrators who handle user offboarding. |
| Orphan Data Administrator | List and delete detached objects through the API | Deletion is irreversible. Assign only to administrators responsible for data cleanup. |
| Transformation Configuration Administrator | Create, update, and archive transformation configurations through the API | Configurations are reused across jobs. Assign only to users who maintain ingestion pipelines. |
| Reference Data Administrator | Delete reference genomes and dictionaries through the API | Deletion is irreversible and affects all users. Assign only to responsible Data Owners. |
| Audit Log Administrator | Search and review audit events across the platform via the API | Grants no access to study content, metadata, or files. Only an **Organisation Administrator** can assign it, and it is never assigned automatically. |

## Related

- [Assign and remove roles](../../admin/manage-users/assign-and-remove-roles.md), the workflow for assigning and removing roles.
- [Groups](groups.md), how group roles differ from platform roles.
- [About audit logs](../../odm-api/admin/audit/about-audit-logs.md), what the **Audit Log Administrator** role gives access to.
- [Delete data](../../odm-api/admin/delete-data.md), which role deletes which kind of object.
- [Recover study ownership](../../odm-api/admin/recover-study-ownership.md), what the **Ownership Recovery Administrator** role is for.
