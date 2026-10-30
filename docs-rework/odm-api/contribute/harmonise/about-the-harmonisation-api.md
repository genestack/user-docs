---
diataxis: explanation
tab: odm-api
---

# About the Harmonisation API

The Harmonisation API is the ODM API for Harmonise: it lets you start Harmonise runs, steer them one step at a time, finish them, and read them back once they are over. It also holds the LLM credentials your runs use, and the LLM providers and models those credentials choose from. The ODM user interface calls the same API, so everything the Harmonise pages do can be scripted.

For what Harmonise is and how a run behaves, see [About Harmonise](../../../contribute/harmonise/about-harmonise.md) and [Run lifecycle](../../../contribute/harmonise/run-lifecycle.md). For every endpoint, field and value, see the [Harmonisation API reference](harmonisation-api-reference.md) and the [Harmonisation API in Swagger](/swagger/?urls.primaryName=harmonisation).

!!! note "Harmonise is in development"
    The endpoints that ask a run for a step, and the steps themselves, are early versions and will change. Runs, their states, and LLM credentials and providers are the stable part of the API.

## Resources

The API lives under `/api/v1/harmonisation` and has three resources:

- **Runs**, at `/api/v1/harmonisation/runs`. A run is one working session of Harmonise, which ODM starts as a processing environment of its own. You start a run, ask it for steps, which it takes one at a time, and finish it. Each run is identified by its number: runs are numbered 1, 2, 3, … in the order they start, across the ODM instance.
- **LLM credentials**, at `/api/v1/harmonisation/llm-credentials`. Your own provider, model and API key, which every run you start uses.
- **LLM providers**, at `/api/v1/harmonisation/llm-providers`. The providers, and their models, that credentials choose from.

## Who can do what

Every call needs an API token or an access token; see [Authentication and tokens](../../getting-started/authentication-and-tokens.md).

- **Runs and LLM credentials** are for users in the **Curator** group. A Curator sees and steers only the runs they started, and reads and changes only their own credentials. Other users get `403 Forbidden`.
- **LLM providers** can be listed by Curators and by holders of the **Harmonisation Administrator** permission. Only Harmonisation Administrators can add, change or remove them, because a provider's base URL is where every run of a Curator who chooses it sends their key.

## A run works as you

When you start a run, ODM creates an API token for you, named `Harmonise-<run id>`, and the run calls ODM with it: whatever it reads or writes in ODM, it does with your permissions. The token is listed among your tokens while the run is open, and ODM deletes it once the run is over.

## Credentials are taken when a run starts

You cannot start a run without LLM credentials that ODM can use: the start is refused with `409 Conflict`, and nothing is created. A run takes your credentials as they are when it starts and keeps them to its end, so credentials you save, change or delete later apply to the next run, not to the runs already open. ODM never returns your key: credentials are read back without it.

## Runs are kept

Runs are never deleted, and the API has no `DELETE` for them. A run that is over reads as it did: its status, times and steps, with what each step found or imported. The list of runs returns every run you started, newest first, those that are over included.

A run's technical log is not part of the API. The run writes it to the logs of the cluster ODM runs on, where your administrator can read it.

## When the API is unavailable

Runs depend on the cluster their processing environments run on, and their history is kept in ODM's analytics database. When either cannot be reached, calls about runs fail with `503 Service Unavailable`; retry them later.

## Related

- [How to run Harmonise via the API](how-to-run-harmonise-via-the-api.md), the end-to-end steps of a run.
- [Manage LLM credentials via the API](manage-llm-credentials-via-the-api.md), your credentials and, for Harmonisation Administrators, the providers.
- [Harmonisation API reference](harmonisation-api-reference.md), every endpoint, field and value.
