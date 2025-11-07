# Users

## Creation

* With **Single Sign-On (SSO)** configured, new users are created automatically upon their first login.
* Detailed instructions for identity provider integration are available in the
[Open Data Manager Administrator Documentation](https://genestack.github.io/admin-docs/latest/home/single-sign-on/sso/).

## Default Access

Newly created users have **immediate access** to studies shared with everyone in the organisation.

## Group Membership

To gain additional rights, users must be added to groups:

* **View group-specific studies** (beyond those shared with all users).
* **Contribute to data** (import new data or curate existing data).

## Lifecycle Management

* Once created, a user **cannot be deleted** from the system.
* Users can, however, be **deactivated** to remove their access.

## Technical Users

* On a fresh **installation** of ODM, a small number of **technical user accounts** are created automatically.
* These accounts support **integration, automated testing, and system configuration**.
They are not intended for day-to-day user activity.
* Passwords for technical users can be changed at any time for **security reasons**.

| User                           | State        | Role                                               |
|--------------------------------|--------------|----------------------------------------------------|
| <root@genestack.com>           | Active       | Superadmin                                         |
| <public@genestack.com>         | Active       | Loading public data, ontologies, setting templates |
| <tester_curator@genestack.com> | Deactivated  | Automated testing upon installation                |
| <tester_user@genestack.com>    | Deactivated  | Automated testing upon installation                |
