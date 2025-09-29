# Getting Access Token (Azure)

This guide explains how to authenticate against the ODM API protected by Azure AD using a **Bearer token**.
We’ll walk through installing the Azure CLI, obtaining the token, and then passing it in request headers.

---

## 0. Prerequisites

Before starting, ensure you have the following:

1. **Azure CLI installed**  
   Follow the official installation guide:
   👉 [Install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

2. **Application ID required for login**  
   It identifies the registered application you're requesting a token for.
   It is recommended to get this ID from your ODM Administrator.

---

## 1. Login to Azure with Required Scope

Run the following command to log in with your **Application (Client) ID** scope:

```bash
az login \
  --scope "api://<APPLICATION_ID>/default" \
  --allow-no-subscriptions
```

* A browser window will open to complete the login.
* Select the appropriate **tenant** (if prompted).
* Once logged in, Azure CLI will establish a session with the provided scope.

---

## 2. Retrieve an Access Token

After logging in, request an access token with:

```bash
az account get-access-token \
  --scope "api://<APPLICATION_ID>/default" \
  --query accessToken
```

This will return a long JWT string (the **Bearer token**), for example:

```json
"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIs..."
```

> ⚠️ The token is valid for a limited time (usually 1 hour). You will need to refresh it when expired.

---

## 3. Use the Bearer Token in ODM API Calls

Pass the token in the `Authorization` header when making ODM API requests.
Here’s an example using `curl`:

```bash
curl -X GET \
  "https://<ODM_HOST>/api/v1/as-user/studies" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

Replace `<ODM_HOST>` with the actual ODM address, `<YOUR_ACCESS_TOKEN>` with the value returned from the previous step.

If authentication is successful, you’ll receive a valid JSON response from the API. Example:

```json
{
  "meta": {
    "pagination": {
      "count": 0,
      "total": 0,
      "offset": 0,
      "limit": 2000
    }
  },
  "data": []
}
```
