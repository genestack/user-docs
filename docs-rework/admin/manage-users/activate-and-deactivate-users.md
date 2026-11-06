---
diataxis: how-to
tab: admin
---

# How to activate and deactivate users

This guide explains how to deactivate a user account in ODM, or reactivate one that has previously been deactivated.

## Prerequisites

You must have the **Organisation Administrator** role to change a user's status.

## About deactivation

ODM does not allow user accounts to be deleted, only deactivated. A deactivated user cannot log in and loses access to all ODM resources immediately. Their attribution on prior changes and audit history is preserved intact. For more on how user accounts work, see [Users and accounts](../../overview/access-control/users-and-accounts.md).

> **Note:** only a study owner can transfer their studies, so a deactivated user's studies stay with them. Ask the user to transfer their studies before you deactivate the account. Afterwards, a user with the **Ownership Recovery Administrator** role can reassign them; see [Recover study ownership](../../odm-api/admin/recover-study-ownership.md).

## Deactivate a user

1. Click the three-line menu at the top left of the Dashboard.
2. Select **Users and Roles**.
3. Find the user, using the **Name or email** search field if the list is long.
4. Click the user's row, or its edit button. A panel opens on the right with the user's details.
5. Click **Deactivate**. A confirmation dialog opens with the user's name, email and ID.
6. Click **Deactivate** in the dialog to confirm, or **Cancel** to keep the user active.

The change takes effect as soon as you confirm. A **DEACTIVATED** badge appears next to the user's name, and the button changes to **Activate**. The user keeps their roles and still appears in the list and in search results.

> **Note:** you cannot deactivate your own account, so the button is not shown in your own panel.

## Reactivate a user

Follow steps 1–4 above, then click **Activate**. No confirmation is asked: the user regains access immediately.
