---
diataxis: how-to
tab: admin
---

# How to create and delete groups

This guide explains how to create a new group in ODM and how to delete one you no longer need.

## Prerequisites

Any user can create a group; no special permission is required for group creation.

To delete a group that you did not create (i.e., one you are not the Group Admin of), you need the **Manage groups** permission. Without it, only the Group Admin of a group can delete it. See [Permissions](../../overview/access-control/permissions.md).

For background on how groups work and the default groups that ship with ODM, see [Groups and roles](../../overview/access-control/groups-and-roles.md).

## Create a group

1. Click the three-line menu at the top left of the Dashboard.
2. Select **Groups**.
3. Click **+ New Group**.
4. Enter a name for the group in the window that appears.
5. Click **Create**.

The group is created immediately. The user who created it is automatically assigned as the Group Admin. Every group must have at least one Group Admin at all times.

There is no limit to the number of groups you can create, but avoid creating multiple groups with the same name; it creates confusion when managing sharing and permissions.

## Delete a group

1. Navigate to the group you want to delete.
2. Click the three-dot menu ( ⋮ ) on the right side of the group.
3. Select **Delete group**.
4. Confirm the deletion when prompted.

Deleting a group is permanent and cannot be undone.

> **Important:** do not delete the default **All users** or **Curator** groups. These groups are used by ODM for system-wide sharing and curation access control. Deleting them will disrupt access for all users on the instance.
