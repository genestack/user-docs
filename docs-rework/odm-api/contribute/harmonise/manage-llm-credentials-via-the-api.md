---
diataxis: how-to
tab: odm-api
---

# How to manage LLM credentials via the API

Harmonise runs call a large language model (LLM) with the credentials of the Curator who started them: a provider, a model and their own API key. This guide covers saving, reading and deleting your credentials through the Harmonisation API and, for Harmonisation Administrators, managing the providers and models Curators choose from.

For how runs use credentials, see [About the Harmonisation API](about-the-harmonisation-api.md). For every field, see the [Harmonisation API reference](harmonisation-api-reference.md#llm-credentials).

## Prerequisites

- An API token. See [Authentication and tokens](../../getting-started/authentication-and-tokens.md).
- For your credentials: Curator group membership, and an API key for one of the providers your ODM instance offers.
- For the providers: the **Harmonisation Administrator** permission. See [Manage LLM providers](../../../admin/manage-users/manage-llm-providers.md).

## List the providers and models

```text
GET /api/v1/harmonisation/llm-providers
```

Returns the providers, ordered by name, each with its models:

```json
[
  {
    "id": "anthropic",
    "name": "Anthropic",
    "api": "ANTHROPIC",
    "baseUrl": "https://api.anthropic.com",
    "models": ["claude-sonnet-5-5"],
    "updatedAt": "2026-10-26T12:00:00Z"
  }
]
```

Note the `id` of the provider you have a key for, and the model you want.

## Save your credentials

```text
PUT /api/v1/harmonisation/llm-credentials
```

```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-5-5",
  "apiKey": "<your key>"
}
```

The response, `200 OK`, is your credentials, without the key, which ODM never returns. Saving replaces any credentials saved before, and makes no call to the provider: to find out whether it accepts the key, have a run check it (`POST /api/v1/harmonisation/runs/{id}/check-llm`; see [How to run Harmonise via the API](how-to-run-harmonise-via-the-api.md#step-4-ask-the-run-for-steps)).

`apiKey` is required when you have no credentials saved, or when you change provider. To change only the model, leave `apiKey` out: the saved key stays. A key is 1 to 1024 printable ASCII characters, without spaces. An unknown provider, a model it does not list, or an invalid or missing key is refused with `400 Bad Request`.

Runs that have already started keep the credentials they started with: what you save applies to the runs you start afterwards.

## Read your credentials

```text
GET /api/v1/harmonisation/llm-credentials
```

```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-5-5",
  "status": "USABLE",
  "updatedAt": "2026-10-26T12:00:00Z"
}
```

A run can start only while `status` is `USABLE`. `PROVIDER_REMOVED` or `MODEL_REMOVED` means a Harmonisation Administrator removed your provider or model since you saved them: save credentials again with another. `404 Not Found` means you have none saved.

## Delete your credentials

```text
DELETE /api/v1/harmonisation/llm-credentials
```

Returns `204 No Content`. You cannot start a run until you save credentials again; runs already started keep theirs.

## Manage the providers

Holders of the **Harmonisation Administrator** permission add, change and remove providers. Other users get `403 Forbidden`.

To add a provider:

```text
POST /api/v1/harmonisation/llm-providers
```

```json
{
  "id": "my-provider",
  "name": "My provider",
  "api": "OPENAI",
  "baseUrl": "https://llm.example.com",
  "models": ["model-a", "model-b"]
}
```

- `id` is fixed once the provider is added: lowercase letters, digits and hyphens, at most 64 characters. An `id` in use is refused with `409 Conflict`.
- `api` is the API runs speak to the provider: `ANTHROPIC`, or `OPENAI`, which also covers endpoints compatible with OpenAI's API.
- `baseUrl` is the root of the provider's API: `https`, without a version, user info, query or fragment, for example `https://api.anthropic.com`. Every run of a Curator who chooses this provider sends their key there.
- `models` lists at least one model, as the provider names it.

To change a provider, send the whole provider again, with the same `id`:

```text
PUT /api/v1/harmonisation/llm-providers/{id}
```

To remove a provider and its models:

```text
DELETE /api/v1/harmonisation/llm-providers/{id}
```

Curators who chose a provider you remove, or a model you no longer list, keep their credentials, which then read `PROVIDER_REMOVED` or `MODEL_REMOVED`, and cannot start runs until they choose again. Runs already started keep what they started with.

## Related

- [Save your LLM credentials](../../../contribute/harmonise/save-your-llm-credentials.md), the same for your credentials in the user interface.
- [Manage LLM providers](../../../admin/manage-users/manage-llm-providers.md), the same for providers in the user interface.
- [Harmonisation API reference](harmonisation-api-reference.md), every endpoint, field and value.
