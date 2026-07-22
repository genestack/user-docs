---
diataxis: how-to
tab: api-libraries
---

# Create users with the SDK

This guide explains how to create user accounts in ODM using the `odm-create-users` script.

## Prerequisites

- Configured ODM SDK. See [Configure](../configure.md).
- A `users.tsv` file listing the users to create.

## Steps

1. Edit your `users.tsv` file in a text editor. List one user per line with email and name separated by a tab.

2. Run the script, replacing the host name with your ODM instance address:

   ```shell
   odm-create-users -H localhost:8080
   ```

   Alternatively, use the alias created during SDK setup:

   ```shell
   odm-create-users -u your_alias
   ```

3. The script creates the user accounts and prints their generated passwords:

   ```text
   alice@alphacorp.com    uNgp4F6C    Alice
   bob@alphacorp.com      xI3AOf2h    Bob
   ```

Share the passwords with the new users so they can log in and set their own passwords.
