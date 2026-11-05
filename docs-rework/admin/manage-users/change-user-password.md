---
diataxis: how-to
tab: admin
---

# How to change a user's password

This guide explains how to change another user's password in ODM as an administrator.

> **Warning:** this guide does not apply to accounts that sign in only with SSO or are synchronised through [SCIM](../scim-integration.md). Such accounts have no password stored in ODM, so their panel has no **Change password**. For more on sign-in methods, see [Users and accounts](../../overview/access-control/users-and-accounts.md#sign-in-methods).

## Prerequisites

- You must have the **Organisation Administrator** role.
- The user must be active. The panel of a deactivated user has no **Change password**.

## Steps

1. Click the three-line menu at the top left of the Dashboard.
2. Select **Users and Roles**.
3. Find the user whose password you want to change, using the **Name or email** search field if the list is long.
4. Click the user's row, or its edit button. A panel opens on the right with the user's details.
5. Click **Change password**. The **Change password** window opens with the user's name, email and ID.
6. In step 1 of 2, **Confirm it's you**, enter your own password under **Your password** and click **Continue**. If the password is wrong, the window shows **Incorrect password. Try again.**
7. In step 2 of 2, **New password**, enter the new password, then enter it again under **Confirm new password**. The password must have:
    - at least 8 characters
    - a capital letter
    - a lower-case letter
    - a number

    Each requirement turns green once the password meets it, and the window shows whether the two passwords match.

8. Click **Save**.

> **Note:** in your own panel, **Change password** opens **Change your password** instead. There you confirm your current password, and the new password must differ from it.
