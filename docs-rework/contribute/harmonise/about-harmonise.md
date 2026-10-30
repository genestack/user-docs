---
diataxis: explanation
tab: contribute
---

# About Harmonise

Harmonise prepares the raw files of a study for ODM with the help of a large language model (LLM). It reads the study's files from the S3 storage your ODM instance is set up with, and writes what it produces into ODM as you. You work with Harmonise in runs: you start a run, steer it, and finish it when you are done.

!!! note "Harmonise is in development"
    What a run does between its start and its finish, and the run page that shows it, are early versions and will change. This section describes what stays: runs, their lifecycle, and the LLM credentials they use.

## Runs

A run is one working session of Harmonise. When you start a run, ODM starts a processing environment for it, separate from ODM itself, and the run waits for your instructions. It takes them one at a time, in the order you give them: an instruction you give while another is in progress waits for its turn. Each instruction is a step of the run, and the run page lists them with their results.

A run stays open until you finish it. There is no cancel: a step, once started, runs to its end, and finishing a run waits for it. For the states a run goes through, see [Run lifecycle](run-lifecycle.md).

Runs are numbered 1, 2, 3, … in the order they start, across your ODM instance, and named by their number, for example *Run 42*. A run is yours: only the Curator who started it sees it and steers it.

## A run works as you

When you start a run, ODM creates an API token for you, named `Harmonise-<run number>`, and the run calls ODM with it. Whatever a run reads or writes in ODM, it does with your permissions, and whatever it creates is yours, as if you had done it yourself. The token is listed among your API tokens on your Profile page while the run is open, and ODM deletes it once the run is over.

## The LLM and your key

A run calls an LLM with your own API key, for a provider and a model you choose on your Profile page. The calls go from the run straight to the provider, so the provider bills them to your account with it. Which providers and models you can choose from is up to a user with the **Harmonisation Administrator** permission; see [Manage LLM providers](../../admin/manage-users/manage-llm-providers.md).

You cannot start a run until you have saved credentials that ODM can use. A run takes your credentials as they are when it starts and keeps them to its end: credentials you save later apply to your next run. ODM never shows your key again once it is saved. See [Save your LLM credentials](save-your-llm-credentials.md).

## Runs are kept

A run is never deleted. ODM keeps its record for good: its status and times, the steps you asked for and their results, and who asked for what and when. Once a run is over and its processing environment is gone, its page reads as it did, and the Harmonise page still lists it.

The run's own technical log is not shown in ODM: it goes to the logs of the cluster ODM runs on, where your administrator can read it.

## Related

- [Run lifecycle](run-lifecycle.md), the states a run goes through.
- [Start and finish a run](start-and-finish-a-run.md), the steps to start a run and to finish it.
- [Save your LLM credentials](save-your-llm-credentials.md), the credentials every run needs.
- [About the Harmonisation API](../../odm-api/contribute/harmonise/about-the-harmonisation-api.md), the same operations through the API.
