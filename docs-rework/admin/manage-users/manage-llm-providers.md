---
diataxis: how-to
tab: admin
---

# How to manage LLM providers

Harmonise runs call a large language model (LLM) with each Curator's own API key, for a provider and a model the Curator chooses on their Profile page. This guide explains how to set up the providers and models Curators choose from, and who may do it.

## The Harmonisation Administrator role

Managing LLM providers takes the **Harmonisation Administrator** role, whose description in **Users and Roles** reads "Manages the LLM providers and models Curators choose from for Harmonise." It is the only thing the role allows: it grants no access to study data, and holders who are not in the Curator group do not see Harmonise itself.

The system account `root@genestack.com` holds it by default. Any other user gets it like any other role, from a user with the **Organisation Administrator** role; see [Assign and remove roles](assign-and-remove-roles.md).

Assign it sparingly, and to users who do not start Harmonise runs themselves. A provider's base URL is where every run of a Curator who chooses that provider sends their API key, and a run acts in ODM with the full identity of the Curator who started it: a run of a Curator who holds the role could change a provider's base URL too, and collect the keys of the Curators who choose it. Since `root@genestack.com` is a Curator and holds the role by default, consider removing it from root if root starts runs.

## The default providers

Every ODM instance starts with two providers, which you can change or remove like any other:

| Id | Name | API | Base URL | Model |
| --- | --- | --- | --- | --- |
| `anthropic` | Anthropic | Anthropic | `https://api.anthropic.com` | `claude-sonnet-5-5` |
| `openai` | OpenAI | OpenAI or compatible | `https://api.openai.com` | `gpt-6-astra` |

## Prerequisites

You must have the **Harmonisation Administrator** role.

## Open the LLM Providers page

Click the three-line menu at the top left of the Dashboard and select **LLM Providers**. The page lists every provider, with its API, base URL and models.

## Add a provider

1. Click **Add provider**.
2. Fill in the provider:
    - **Id**: a short identifier of lowercase letters, digits and hyphens, at most 64 characters. It cannot be changed later.
    - **Name**: the name Curators see.
    - **API**: the API runs speak to the provider: **Anthropic**, or **OpenAI or compatible** for OpenAI and services compatible with its API.
    - **Base URL**: the root of the provider's API, starting with `https://` and without a version, for example `https://api.anthropic.com`.
    - **Models**: one per line, as the provider names them.
3. Click **Add**.

Curators can choose the provider and its models on their Profile page at once.

## Edit a provider

Click **Edit** in the provider's row, change its name, API, base URL or models, and click **Save**. Its id stays.

Curators who chose a model you removed keep their credentials, but cannot start a run until they choose another: their Profile page says *Your model is no longer offered: choose another*.

## Delete a provider

Click **Delete** in the provider's row and confirm. The provider and its models are removed.

Curators who chose it keep their credentials, but cannot start a run until they choose another provider: their Profile page says *Your provider is no longer offered: choose another*.

Runs that have already started are not affected by any change here: they keep the provider and model they started with.

## Related

- [Save your LLM credentials](../../contribute/harmonise/save-your-llm-credentials.md), how Curators choose a provider and a model.
- [About Harmonise](../../contribute/harmonise/about-harmonise.md), how runs use the LLM.
- [Manage LLM credentials via the API](../../odm-api/contribute/harmonise/manage-llm-credentials-via-the-api.md#manage-the-providers), managing providers through the API.
