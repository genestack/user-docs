---
diataxis: reference
tab: overview
---

# Users and accounts

## Creation

With Single Sign-On (SSO) configured, new users are created automatically upon their first login. Detailed instructions for identity provider integration are available in the [ODM Administrator Documentation](https://genestack.github.io/admin-docs/latest/home/single-sign-on/sso/). Automated provisioning via AD/SCIM is also supported. See [SCIM integration](../../admin/scim-integration.md).

## Sign-in methods

An ODM account uses one of two sign-in methods.

- Password-based accounts sign in with an email and a password stored in ODM. On instances without SSO, an administrator creates these accounts in **Users and Roles**. The [technical users](#technical-users), including root, also have password-based accounts. The account owner can change the password in their profile, or an administrator can change it for them. See [How to change a user's password](../../admin/manage-users/change-user-password.md).
- SSO-only accounts sign in through the organisation's identity provider. ODM creates them on the user's first SSO login, or receives them through [SCIM](../../admin/scim-integration.md). ODM stores no password for these accounts, so neither the user nor an administrator can set or change one in ODM. The identity provider manages their credentials.

## Default access

Newly created users have immediate access to studies shared with everyone in the organisation. Access beyond that requires group membership.

## Group membership

To gain additional rights (viewing group-specific studies or contributing data), users must be added to groups. See [Groups](groups.md) for how groups and the Curator group grant access.

## Lifecycle

Once created, a user cannot be deleted from the system. Users can be deactivated to remove their access. A deactivated user's studies can no longer be transferred by their owner; they can be reassigned through [ownership recovery](../../odm-api/admin/recover-study-ownership.md). See [Activate and deactivate users](../../admin/manage-users/activate-and-deactivate-users.md) for the procedure.

## Technical users

On a fresh installation of ODM, a small number of technical user accounts are created automatically. These accounts support integration, automated testing, and system configuration and are not intended for day-to-day use. Passwords for technical users can be changed at any time.

| User | State | Purpose |
|---|---|---|
| <root@genestack.com> | Active | Organisation Administrator |
| <public@genestack.com> | Active | Loading public data, ontologies, setting templates |
| <tester_curator@genestack.com> | Deactivated | Automated testing upon installation |
| <tester_user@genestack.com> | Deactivated | Automated testing upon installation |

## Profile

Users access their own profile via the top-right menu in the ODM interface. The profile window shows whether the user is an administrator, which groups they belong to, and allows them to change their password and manage API tokens. For token management, see [Authentication and tokens](../../odm-api/getting-started/authentication-and-tokens.md).
