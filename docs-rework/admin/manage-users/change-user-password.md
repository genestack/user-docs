---
diataxis: how-to
tab: admin
---

# How to change a user's password

This guide explains how to change the password of another user's account as an administrator in ODM.

## Prerequisites

- You must have the **Organisation Administrator** role.
- Your administrator account must have a password set. If your account uses SSO as its only login method, you do not have a stored password, and **Change password** is not shown in any user's panel. Use the root account in that case. For more on account types, see [Users and accounts](../../overview/access-control/users-and-accounts.md).
- The user must be active and have a password. **Change password** is not shown for a deactivated user, or for a user who signs in only with SSO.

## Steps

1. Click the three-line menu at the top left of the Dashboard.
2. Select **Users and Roles**.
3. Find the user whose password you want to change, using the **Name or email** search field if the list is long.
4. Click the user's row, or its edit button. A panel opens on the right with the user's details.
5. Click **Change password**. The **Change password** window opens, showing the user's name, email and ID.
6. Step 1 of 2, **Confirm it's you**: enter your own password under **Your password** and click **Continue**. If the password is wrong, the window shows **Incorrect password. Try again.**
7. Step 2 of 2, **New password**: enter the new password and enter it again under **Confirm new password**. The password must have:
    - at least 8 characters
    - a capital letter
    - a lower-case letter
    - a number

    Each requirement turns green once the password meets it, and the window shows whether the two passwords match.

8. Click **Save**.

A confirmation message such as **Password for Jane Doe updated** appears when the password has been changed. To leave without changing it, click **Cancel** or the close button: nothing you entered is kept.

> **Note:** in your own panel, **Change password** opens **Change your password**, where you change your own password: you confirm your current password, and the new one must differ from it.
