---
diataxis: how-to
tab: contribute
---

# How to share a study

This guide explains how to share a study with one or more user groups in ODM.

## Prerequisites

- You must own the study to share or unshare it. See [Sharing and ownership](../../overview/access-control/sharing-and-ownership.md) for the ownership model.
- You must be a member of the groups you want to share the study with.

Studies in ODM are shared with groups, not with individual users. For an explanation of how groups work, see [Groups and roles](../../overview/access-control/groups-and-roles.md).

## Share from the Study Browser

1. Click the three-dot menu ( ⋮ ) next to the study title in the Study Browser.
2. Select **Share**.
3. The sharing dialog shows which groups currently have access to the study.
4. Select the additional group or groups you want to grant access to.
5. Click **Share**.

Members of the newly added group will be able to find the study using the **Shared with me** filter in the Study Browser.

## Share from the Metadata Editor

The sharing dialog is also accessible from within an open study:

1. Click the study name or the folder icon at the top of the Metadata Editor page.
2. Select **Share**.
3. The same sharing dialog appears. Follow steps 3–5 above.

## Revoke access

To remove a group's access, open the Share dialog using either method above and deselect the group, then confirm.

## Share via the SDK

To share a study programmatically using the ODM SDK, see [Share a study](../../api-libraries/odm-sdk/study/share-a-study.md).

To transfer ownership of a study rather than sharing it, see [Transfer study ownership](transfer-study-ownership.md).
