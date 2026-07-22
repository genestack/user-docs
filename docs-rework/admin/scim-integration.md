---
diataxis: explanation
tab: admin
---

# SCIM integration

ODM provides RESTful APIs for user and group management based on the SCIM 2.0 provisioning standard. These APIs allow seamless integration with external identity providers such as Active Directory, enabling automated and synchronised access management.

## Benefits

Connecting ODM to an identity provider via SCIM establishes a single central entry point for access control, which reduces duplication and the risk of errors. It enables reliable, efficient user lifecycle management across the organisation. SCIM integration is recommended for all customers whose identity providers support SCIM 2.0.

## How it works with Active Directory

ODM's SCIM endpoints allow Active Directory (AD) to act as the authoritative system for user management. Administrators manage users and groups in AD: creating accounts, adding or removing users from groups, and deactivating users. Changes propagate to ODM automatically on a scheduled synchronisation configured in AD.

## Flexibility

ODM supports both SCIM-provisioned groups and locally-created groups. This means you can use AD to manage your organisation-wide groups via SCIM while still creating temporary project groups directly in ODM for restricted sharing. For example, a short-term project group can be created in ODM and used to share a study with a specific subset of users, independently of your AD structure.

## Setup

Detailed setup instructions are documented in the Genestack admin documentation: [Enterprise applications SCIM provisioning](https://genestack.github.io/admin-docs/latest/home/single-sign-on/scim/azure/#configure-user-and-group-provisioning).

ODM's SCIM endpoints follow the SCIM 2.0 standard and are compatible with any identity provider that supports SCIM 2.0. Test the integration in a non-production environment before rolling it out, as each identity provider has its own specific configuration requirements.

## Recommendation

Run user and group synchronisation in AD on behalf of a user who has the **Manage groups** permission in ODM. This ensures the synchronisation account can see and edit all groups on the instance, regardless of group membership.

For manual user management without SCIM, see [Create users](manage-users/create-users.md). For context on how user accounts and groups work in ODM, see [Users and accounts](../overview/access-control/users-and-accounts.md) and [Groups and roles](../overview/access-control/groups-and-roles.md).
