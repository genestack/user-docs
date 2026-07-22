---
diataxis: how-to
tab: admin
---

# How to grant and revoke permissions

This guide explains how to assign or remove permissions for a user in ODM.

## Prerequisites

You must have the **Manage organisation** permission. This permission controls access to the Users and Permissions panel where all permission management takes place.

For a full description of what each permission allows, see [Permissions](../../overview/access-control/permissions.md).

## Steps

1. Click the three-line menu at the top left of the Dashboard.
2. Select **Users and Permissions**. A window opens showing all users in the organisation.
3. Use the search bar to find the user you want to update.
4. Tick the checkbox next to a permission name to grant that permission. Untick it to revoke.

The available permissions are: **Manage organisation**, **Manage groups**, **Set up templates**, **Access all data**, and **Configure facets**. Hover over any permission name to see a brief description of what it enables.

Changes take effect immediately. The user may need to refresh their session before the updated permissions are reflected in their UI.

> **Note on Manage organisation:** granting this permission is significant because it allows the recipient to grant permissions to other users. Assign it sparingly, and only to users who need to perform admin tasks.
