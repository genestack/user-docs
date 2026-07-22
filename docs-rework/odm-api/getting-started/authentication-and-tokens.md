---
diataxis: how-to
tab: odm-api
---

# Authentication and tokens

Every ODM API request requires an authorisation token. The token determines which data you can retrieve and which operations you are permitted to perform. ODM supports two token types: a Genestack API token (personal access token) and an Identity Provider access token such as an Azure AD Bearer token.

## Generate a Genestack API token

1. Sign in to ODM via a web browser.
2. Click your username or email address in the top-right corner and select **Profile**.
3. Under API tokens, click **Create new token**.
4. Enter a name for the token when prompted. The token value is displayed immediately after you confirm creation. (Since release 1.62, token creation no longer requires an email step; the value appears on-screen.)
5. Download the token as a plain-text file (.txt) or copy the value directly.
6. Store the token securely. You will not be able to view it again after closing the dialog.

### Token capabilities

A single user account can have multiple active tokens. Each token is permanent; there is no expiration date. You can revoke any token at any time from your Profile page. Use the HTTP header `Genestack-Api-Token` to send the token with API requests.

## Use a Genestack API token

You can supply a Genestack API token in three ways, depending on how you are calling the API.

**In Swagger UI**

Click **Authorize**, select **Genestack API token**, paste the token value, and close the dialog. See [Make your first request in Swagger](make-your-first-request.md) for the full Swagger workflow.

**In curl**

Send the token in the `Genestack-Api-Token` header:

```bash
curl -X GET "https://<ODM_HOST>/api/v1/as-user/studies" \
  -H "Genestack-Api-Token: <YOUR_TOKEN>"
```

**In the ODM SDK**

Run `odm-user-setup -H https://<ODM_HOST>` and follow the prompts. See [Configure the ODM SDK](../../api-libraries/odm-sdk/configure.md) for full setup instructions.

## Identity Provider access tokens

ODM also supports access tokens issued by an external identity provider such as Azure AD. Send these using the `Authorization` header:

```
Authorization: Bearer <YOUR_ACCESS_TOKEN>
```

Additional configuration on the ODM instance is required to enable Identity Provider token usage. For the Azure AD workflow specifically, see [Get an Azure access token](get-an-azure-access-token.md).

## Token precedence

If both a `Genestack-Api-Token` header and an `Authorization: Bearer` header are present in the same request, the Identity Provider access token takes precedence. For security and consistency, enterprise deployments should prefer Identity Provider tokens where available.

## Why tokens matter

API tokens provide a secure method for authenticating users, ensuring only those with valid credentials can access data. They enforce access control by respecting each user's permissions and group memberships. They also enable auditability: all API interactions are logged and traceable to the token's issuing user. Finally, they enable seamless automated workflows by eliminating the need for manual re-authentication on each request.
