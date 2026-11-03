---
diataxis: how-to
tab: admin
---

# Enable the MCP server

The ODM MCP server lets AI assistants that support the [Model Context Protocol](https://modelcontextprotocol.io) (MCP) search and read ODM data for the user who is signed in to them. It ships with the ODM Helm chart from release 1.65 and is off by default. This guide is for the administrator who deploys ODM.

## How it works

- The MCP server runs next to ODM and is reached through ODM's own address: MCP clients connect to `https://<ODM_HOST>/mcp`.
- Users sign in with Microsoft Entra ID (Azure AD), through the application ODM already uses for Microsoft sign-in. For every request, the MCP server exchanges the user's token for one scoped to ODM (On-Behalf-Of), so the assistant sees exactly what the user can see in ODM, no more. MCP clients never receive the Microsoft tokens.
- Its tools only search and read: an assistant cannot change data in ODM through it.

## Prerequisites

- ODM 1.65 or later, deployed with the ODM Helm chart.
- Microsoft sign-in configured for ODM, with ODM accepting Azure access tokens for `api://<APPLICATION_ID>/default` (see [Get an Azure access token](../odm-api/getting-started/get-an-azure-access-token.md)).
- In the Azure AD application ODM uses (your Azure administrator does this):
    - Under **Authentication**, a **Web** redirect URI `https://<ODM_HOST>/auth/callback`.
    - Under **Expose an API**, the scope `user_impersonation` next to `default`, both under `api://<APPLICATION_ID>`.
    - A client secret. The one ODM uses for Microsoft sign-in will do.

## Step 1: Add the MCP server to your values

Add the tenant ID, application (client) ID and client secret of that application:

```yaml
mcp:
  enabled: true
  envVars:
    AZURE_TENANT_ID: "<TENANT_ID>"
    AZURE_CLIENT_ID: "<APPLICATION_ID>"
    AZURE_CLIENT_SECRET: "<CLIENT_SECRET>"
```

To keep the secret out of your values, create a Kubernetes Secret with those three keys in ODM's namespace and name it instead:

```yaml
mcp:
  enabled: true
  envVarsFromSecrets:
    - odm-mcp-creds
```

With `envVars`, the chart refuses to render if any of the three is missing. It cannot read a Secret, so with `envVarsFromSecrets`, make sure the Secret holds all three keys: without them the MCP server does not start, or no user can sign in.

## Step 2: Upgrade the release

Upgrade ODM with these values as you usually do, for example:

```bash
helm upgrade <RELEASE> <ODM_CHART> \
  --version <VERSION> \
  --namespace <NAMESPACE> \
  --values my-values.yaml
```

This adds an `mcp` Deployment and Service, and routes these paths on `https://<ODM_HOST>` to it: `/mcp`, and the OAuth endpoints MCP clients sign in through, `/.well-known/oauth-authorization-server`, `/.well-known/oauth-protected-resource`, `/authorize`, `/token`, `/register`, `/consent` and `/auth/callback`.

## Step 3: Check that it answers

```bash
curl https://<ODM_HOST>/.well-known/oauth-protected-resource/mcp
```

The response names `https://<ODM_HOST>/mcp` as the resource and `user_impersonation` as its scope. Then give your users the address `https://<ODM_HOST>/mcp` and [Connect an AI assistant to ODM](../explore/connect-an-ai-assistant.md).

## Good to know

- **Network access.** An MCP client that runs on the user's machine, such as Claude Code or VS Code, reaches ODM as the browser does. An assistant hosted by an AI provider connects from the provider's servers, so those servers must reach `https://<ODM_HOST>` too.
- **Sign-ins do not survive a restart.** The MCP server keeps registered clients and sign-ins in its pod. When the pod is replaced, during an upgrade for example, users sign in again.
- **No API tokens.** The MCP server only runs with user sign-in here: the chart refuses `ODM_API_TOKEN` in `mcp.envVars`, since with a token everyone would act as that one user.
