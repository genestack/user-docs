---
diataxis: how-to
tab: admin
---

# How to create a user

This guide explains how to add a new user to your ODM instance via the user interface.

## Prerequisites

You must have the **Manage organisation** permission to create users. See [Permissions](../../overview/access-control/permissions.md) for the full list of permissions and what they control.

> **Note:** if your ODM instance uses Single Sign-On (SSO), new users are created automatically the first time they log in. Manual user creation is for non-SSO instances.

## Steps

1. Click the three-line menu at the top left of the Dashboard.
2. Select **Users and Permissions**. A window opens listing all users in the instance.
3. Click **+ New user**.
4. Fill in the user's details, including their email address and name.
5. Click **Add** to confirm.

ODM detects if a user with that email address has been previously added and will alert you if there is a conflict.

## Next steps

After creating a user, you may want to:

- Grant permissions to the user. See [Grant and revoke permissions](grant-and-revoke-permissions.md).
- Deactivate a user who should no longer have access. See [Activate and deactivate users](activate-and-deactivate-users.md).
- Set up automated provisioning via SCIM. See [SCIM integration](../scim-integration.md).
