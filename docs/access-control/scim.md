# Access Management via SCIM APIs

## Overview

* ODM provides RESTful APIs for user and group management, based on the SCIM 2.0
provisioning standard.
* These APIs allow seamless integration with identity providers (such as Active Directory),
enabling automated and synchronized access management.

## Benefits

* Establishes one central entry point for access control, reducing duplication and errors.
Ensures reliable and efficient user lifecycle management across the organisation.
* Recommended for all customers whose identity providers support SCIM 2.0.

## Workflow with Active Directory

* ODM’s SCIM endpoints allow Active Directory (AD) to be the authoritative system for user
management.
* Administrators manage users in AD, where they can:
    * Create users and groups.
    * Add or remove users from groups.
    * Deactivate users.
* Changes are automatically propagated to ODM on a scheduled sync configured in AD.

## Flexibility

* In addition to AD-provisioned groups, ODM also supports locally created groups for project-specific sharing needs.
* Example: a temporary project group can be created in ODM and used to share studies with a restricted set of users.

For more detail, see [Enterprise applications SCIM provisioning](https://genestack.github.io/admin-docs/latest/home/single-sign-on/scim/azure/#configure-user-and-group-provisioning).
