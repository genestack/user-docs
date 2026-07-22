---
diataxis: how-to
tab: contribute
---

# How to transfer study ownership

This guide explains how to transfer ownership of a study to another user in ODM.

## Who can transfer ownership

The following users may initiate an ownership transfer:

| Initiator | Conditions | Permitted? |
|---|---|:---:|
| Current Study Owner | Always | Yes |
| User with Manage organisation and Access all data | Study is not shared with the user | Yes |
| User with Manage organisation (with access to the study) | Study is shared with the user | Yes |
| Any other user | — | No |

For the full access control model, see [Sharing and ownership](../../overview/access-control/sharing-and-ownership.md).

The target of the transfer must be an active user account. You cannot transfer to a deactivated account.

## Steps

1. Open the study in the Metadata Editor.
2. Click the study name to open the study menu.
3. Hover over the **Owner** option in the study menu.
4. Select **Transfer ownership**. This option is only visible if you meet the criteria in the table above.
5. Choose the new owner from the active-user list. The dropdown is searchable.
6. Click **Assign new owner** in the pop-up to complete the transfer.

## What happens after transfer

The Owner field updates immediately. The new owner receives full access to the study and all related objects across all versions. The previous owner loses access unless the study is explicitly shared back with them or a group they belong to. See [Share a study](share-a-study.md).

Each transfer creates a **Changing Ownership** entry in the study's metadata version history. This entry captures the previous owner, the new owner, the user who initiated the transfer, and the date and time. These entries are informational only. You cannot roll back to a prior owner from the version history window. To change ownership again, perform a new transfer.

## Current limitation

In this release, ownership transfer operates one study at a time. There is no bulk multi-study transfer interface.
