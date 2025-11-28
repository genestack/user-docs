# Permissions

## Overview

* Once a user is created, permissions can be assigned in the **Users and Permissions** section.
* To grant or revoke permissions, a user must have the **Manage organization** permission.
* The system superuser account `root@genestack.com` is created by default with full management rights.

## Permission Types

| Permission          | Actions                                                                                                               | Recommendation                                                                              |
|---------------------|-----------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Manage organization | - Manage permissions <br/> - Manage study ownership <br/> - Create and deactivate users <br/> - Change user passwords | This is a **powerful system-level permission**. Grant only to a few trusted administrators. |
| Set up templates    | - Create new templates <br/> - Alter existing templates                                                               | Changes affect **all users**. Should be assigned only to responsible **Data Owners**.       |
| Configure facets    | Set desired list and order of facets in the Study Browser                                                             | Changes affect **all users**. Should be assigned only to responsible **Data Owners**.       |
| Manage groups       | Access and manage all groups, even without admin/membership rights                                                    | Use primarily for integration purposes.                                                     |
| Access all data     | Access to all studies in the system, even if not shared                                                               | Use only for integration or administrative purposes.                                        |
