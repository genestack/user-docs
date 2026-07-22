---
diataxis: reference
tab: overview
---

# Users and accounts

## Creation

With Single Sign-On (SSO) configured, new users are created automatically upon their first login. Detailed instructions for identity provider integration are available in the [ODM Administrator Documentation](https://genestack.github.io/admin-docs/latest/home/single-sign-on/sso/). Automated provisioning via AD/SCIM is also supported. See [SCIM integration](../../admin/scim-integration.md).

## Default access

Newly created users have immediate access to studies shared with everyone in the organisation. Access beyond that requires group membership.

## Group membership

To gain additional rights (viewing group-specific studies or contributing data), users must be added to groups. See [Groups and roles](groups-and-roles.md) for how groups and the Curator group grant access.

## Lifecycle

Once created, a user cannot be deleted from the system. Users can be deactivated to remove their access. See [Activate and deactivate users](../../admin/manage-users/activate-and-deactivate-users.md) for the procedure.

## Technical users

On a fresh installation of ODM, a small number of technical user accounts are created automatically. These accounts support integration, automated testing, and system configuration and are not intended for day-to-day use. Passwords for technical users can be changed at any time.

| User | State | Role |
|---|---|---|
| root@genestack.com | Active | Superadmin |
| public@genestack.com | Active | Loading public data, ontologies, setting templates |
| tester_curator@genestack.com | Deactivated | Automated testing upon installation |
| tester_user@genestack.com | Deactivated | Automated testing upon installation |

## Profile

Users access their own profile via the top-right menu in the ODM interface. The profile window shows whether the user is an administrator, which groups they belong to, and allows them to change their password and manage API tokens. For token management, see [Authentication and tokens](../../odm-api/getting-started/authentication-and-tokens.md).
