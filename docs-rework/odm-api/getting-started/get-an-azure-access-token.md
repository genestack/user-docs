---
diataxis: how-to
tab: odm-api
---

# How to get an Azure access token

This guide explains how to authenticate against the ODM API when your instance is protected by Azure Active Directory, using a Bearer token obtained via the Azure CLI.

For the broader token model and precedence rules, see [Authentication and tokens](authentication-and-tokens.md).

## Prerequisites

- **Azure CLI installed.** Follow the official installation guide: [Install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
- **Application (Client) ID for your ODM instance.** Request this from your ODM Administrator. It identifies the registered application you are requesting a token for.

## Step 1: Log in to Azure with the required scope

```bash
az login \
  --scope "api://<APPLICATION_ID>/default" \
  --allow-no-subscriptions
```

A browser window opens to complete the login. Select the appropriate tenant if prompted. Once logged in, the Azure CLI establishes a session with the provided scope.

## Step 2: Retrieve an access token

```bash
az account get-access-token \
  --scope "api://<APPLICATION_ID>/default" \
  --query accessToken
```

This returns a long JWT string, your Bearer token. The token is valid for approximately one hour.

## Step 3: Use the token in ODM API calls

Pass the token in the `Authorization` header with every request:

```bash
curl -X GET \
  "https://<ODM_HOST>/api/v1/as-user/studies" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

Replace `<ODM_HOST>` with the URL of your ODM instance and `<YOUR_ACCESS_TOKEN>` with the value returned in Step 2. If authentication is successful, you will receive a valid JSON response from the API.

## Token expiration

Azure access tokens expire after approximately one hour. Repeat Steps 1 and 2 to obtain a fresh token when the current one expires.
