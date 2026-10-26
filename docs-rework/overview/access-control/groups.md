---
diataxis: explanation
tab: overview
---

# Groups

## Purpose of groups

Groups in ODM simplify collaboration and data sharing. A group can represent a location, department, or project team, ensuring that data is shared only with the relevant people. Users see only the groups they are members of, unless they hold the **Group Administrator** role.

## Default groups

Upon installation, ODM creates two default groups that should not be removed:

- **All users**: every user in the system is automatically a member of this group.
- **Curator**: a special group that grants edit permissions to its members (see below).

## Group roles

Within any group, there are two roles:

- **Group members**: can access all data shared with their group and can share data with the group. Once added to a group, a user immediately has access to all studies shared with it; removing them revokes that access.
- **Group admins**: can add or remove members and assign roles within their group. Admin rights do not extend to other groups.

A user with the **Group Administrator** platform role can manage all groups system-wide, regardless of membership. This is different from being a group admin: the group admin role applies only within one group, while the Group Administrator role is assigned to a user across the whole instance in the Users and Roles application. See [Roles](roles.md).

### Group Administrator role interactions

| Capability | With Group Administrator role | Without Group Administrator role |
|---|---|---|
| Access the groups list | All groups in the system | Only groups you are a member of |
| Create a new group | Yes | Yes (any user can create a group) |
| Add or remove members | Any group | Only groups you are an admin of |
| Delete a group | Any group | Only groups you are an admin of |

## Curator group

Membership in the **Curator group** grants edit permissions. Curators can import new studies, edit metadata, publish their changes as new metadata versions, and restore an earlier version. Users who are not members of the Curator group are considered researchers: they can browse, search, and download data, and they can view a study's version history, but they cannot contribute.

| User type | Member of Curator group? | Capabilities |
|---|---|---|
| Researcher | No | Browse, search, download, view version history |
| Curator | Yes | All of the above, plus import data, edit metadata, publish new versions, and restore earlier ones |

!!! warning
    Do not delete the Curator group. Users need it to contribute data.

## User personas

The following personas describe how different kinds of users typically interact with the platform. They are not roles that can be assigned:

**Data Consumer**: browses and searches studies, exports data, and visualises results. No contribution capabilities.

**Data Contributor**: creates new studies, curates data, shares data with other users and groups, and imports data. Requires membership in the Curator group.

**Administrator**: manages user accounts and roles, and manages groups.

For the procedures to manage users and groups, see [Manage users](../../admin/manage-users/index.md) and [Manage groups](../../admin/manage-groups/index.md). For the model of how data is shared between users and groups, see [Sharing and ownership](sharing-and-ownership.md).
