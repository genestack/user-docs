---
diataxis: explanation
tab: contribute
---

# About Harmonise

Harmonise prepares the raw files of a study for ODM with the help of a large language model (LLM). It reads the study's files from the S3 storage your ODM instance is set up with, and writes what it produces into ODM as you. You work with Harmonise in runs: you start a run, steer it, and finish it when you are done.

!!! note "Harmonise is in development"
    Harmonise is an early version and will change. It does not yet import expression data, and it offers one template, `public_studies`.

## Runs

A run is one working session of Harmonise. When you start a run, ODM starts a processing environment for it, separate from ODM itself, and the run waits for your instructions. It takes them one at a time, in the order you give them: an instruction you give while another is in progress waits for its turn. Each instruction is a step of the run, and the run page lists them with their results.

A run stays open until you finish it. There is no cancel: a step, once started, runs to its end, and finishing a run waits for it. For the states a run goes through, see [Run lifecycle](run-lifecycle.md).

Runs are numbered 1, 2, 3, … in the order they start, across your ODM instance, and named by their number, for example *Run 42*. A run is yours: only the Curator who started it sees it and steers it.

## Phases, attempts and review

A run takes a study through three phases, in order:

1. **Extract** reads the files of a folder in the storage into tables, and the objects in them, such as samples.
2. **Transform** maps what was extracted to the fields of a template: it plans the mapping, carries out the plan, and checks the result.
3. **Export** writes the harmonised study to the storage, as a package of files, and imports its study and samples into ODM.

Each time a phase runs, it makes an **attempt**, a step of the run named after its phase and number, such as `extract-1` or `transform-2`. When an extract or a transform attempt succeeds, you review what it produced on the run page, then do one of two things:

- **Approve** it, with **Approve and transform** or **Approve and export**. This starts the next phase, built on that attempt: the transformation takes the extraction you approved, and the export the transformation you approved.
- **Request changes** to it, with your comments. This runs the same phase again, as a new attempt that revises the one you reviewed and takes your comments into account.

The run page shows where the review of each attempt stands:

| Review | Meaning |
| --- | --- |
| Awaiting review | The attempt succeeded, and you have not acted on it yet. |
| Approved | You asked for a later phase built on the attempt. |
| Changes requested | You requested changes to the attempt. |
| Superseded | A later attempt of the same phase has succeeded; see [Superseded attempts](#superseded-attempts). |

An attempt is **Approved** or **Changes requested** as soon as you ask, whether or not the attempt you asked for then succeeds.

A separate **Under review** badge marks the one attempt you can act on now: the latest successful attempt of the current phase that is not superseded. It shows beside the attempt's review, usually **Awaiting review**, or **Approved** when the phase built on it failed and you can approve the attempt again or request changes to it.

If both happened, for example you approved an extraction, its transformation failed, and you then requested changes to the extraction, the latest one counts.

### Superseded attempts

Once an attempt of a phase succeeds, every earlier attempt of the same phase is **superseded**. A superseded attempt stays on the run page, with its review, but you can no longer approve it or request changes to it. So each phase always has one attempt you can act on: its latest successful one. An attempt that fails supersedes nothing: the one before it is still the one under review.

### No going back

A run moves forward only. Once a transformation has succeeded, the run takes no more extractions, and once an export has succeeded, no more transformations, and no second export: finish the run. To extract a study again, start a new run.

Transform needs an LLM provider that uses the OpenAI API. Extract works with any provider, but without the OpenAI API it decides how to read each file from the file's name only, and ignores the comments of a request for changes. See [Save your LLM credentials](save-your-llm-credentials.md#which-provider-to-choose).

For the steps, see [How to harmonise a study](harmonise-a-study.md).

## A run works as you

When you start a run, ODM creates an API token for you, named `Harmonise-<run number>`, and the run calls ODM with it. Whatever a run reads or writes in ODM, it does with your permissions, and whatever it creates is yours, as if you had done it yourself: the study and samples an export imports are yours. The token is listed among your API tokens on your Profile page while the run is open, and ODM deletes it once the run is over.

## The LLM and your key

A run calls an LLM with your own API key, for a provider and a model you choose on your Profile page. The calls go from the run straight to the provider, so the provider bills them to your account with it. Which providers and models you can choose from is up to a user with the **Harmonisation Administrator** role; see [Manage LLM providers](../../admin/manage-users/manage-llm-providers.md).

You cannot start a run until you have saved credentials that ODM can use. A run takes your credentials as they are when it starts and keeps them to its end: credentials you save later apply to your next run. ODM never shows your key again once it is saved. See [Save your LLM credentials](save-your-llm-credentials.md).

## Runs are kept

A run is never deleted. ODM keeps its record for good: its status and times, the steps you asked for and their results, every attempt with what you reviewed and the comments you made, and who asked for what and when. Once a run is over and its processing environment is gone, its page reads as it did, and the Harmonise page still lists it.

The run's own technical log is not shown in ODM: it goes to the logs of the cluster ODM runs on, where your administrator can read it.

## Related

- [Run lifecycle](run-lifecycle.md), the states a run goes through.
- [How to harmonise a study](harmonise-a-study.md), the phases step by step.
- [Start and finish a run](start-and-finish-a-run.md), the steps to start a run and to finish it.
- [Save your LLM credentials](save-your-llm-credentials.md), the credentials every run needs.
- [About the Harmonisation API](../../odm-api/contribute/harmonise/about-the-harmonisation-api.md), the same operations through the API.
