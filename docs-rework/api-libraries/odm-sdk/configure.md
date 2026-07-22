---
diataxis: how-to
tab: api-libraries
---

# How to configure ODM SDK

This guide explains how to configure the ODM SDK with your ODM instance and API token.

## Prerequisites

- SDK installed. See [Install](install.md).
- An API token from your ODM instance. See [Authentication and tokens](../../odm-api/getting-started/authentication-and-tokens.md).

## Steps

1. Retrieve an API token (or Bearer token) by logging into ODM and clicking the profile link under your username. Click **Create new token** and save the token value.

2. Start the setup wizard from your terminal:

   ```shell
   odm-user-setup -H https://domain_name/
   ```

3. Type `add` to enter a new user and choose an alias for it.

4. Enter the host name in the format `https://domain_name/`.

5. Select an authentication method and enter your token:

   ```shell
   1) by token
   2) by access token
   3) by email and password
   Select authentication: 1
   Host: https://domain_name/
   Please specify Genestack API token for "my_user":
   ```

6. Type `quit` to exit the setup wizard.

## Using the configured alias

After configuration, you can reference the alias in subsequent SDK commands using `-u <alias>` or specify the host directly with `-H <hostname>`.
