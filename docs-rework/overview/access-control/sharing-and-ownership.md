---
diataxis: explanation
tab: overview
---

# Sharing and ownership

## Study ownership

By default, the user who imports a study into ODM owns it. Owners have full control over sharing and access management for their studies.

## Sharing a study

Owners can share studies only with groups they are members of. Once shared with a group, the study becomes available to all members of that group. A study can be shared with multiple groups simultaneously. The list of groups that have access to a study is visible in the "More Info" section of the Metadata Editor.

## Revoking access

Study owners can revoke access from a group at any time.

## Transferring ownership

Ownership of a study can be transferred to another active user in the system. When ownership is transferred, it cascades to all study-scoped objects: the Study, Samples, Libraries, Preparations, and all associated data objects.

### Who can transfer ownership

| Initiator | Conditions | Allowed? | Notes |
|---|---|:---:|---|
| Current Study Owner | Always | Yes | Owner can transfer regardless of other permissions. |
| User with **Manage organisation** and **Access all data** | Study is not shared with user | Yes | For super-admin use cases. |
| User with **Manage organisation** (with access to the Study) | Study is shared with user | Yes | Covers org-level admins who can see the Study. |
| Any other user | — | No | Not permitted. |

Additional rules:

- The target must be another active user. You cannot transfer to a deactivated account.
- Transfers are one study at a time in the current release.

## Access changes after transfer

The new owner receives full access to the study and all related objects across all versions. The previous owner loses access unless the study is explicitly shared back to them.

## Audit trail

Every transfer generates a "Changing Ownership" entry in the study's metadata version history, capturing the previous owner, new owner, initiating user, and the date and time.

!!! note
    Ownership version history entries are informational only. You cannot roll back to a prior owner from the version history window. To change ownership again, perform a new transfer.

For the UI procedure to share a study or transfer ownership, see [Share a study](../../contribute/sharing/share-a-study.md) and [Transfer study ownership](../../contribute/sharing/transfer-study-ownership.md). For how groups gate access, see [Groups and roles](groups-and-roles.md).
