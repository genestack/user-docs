---
diataxis: how-to
tab: contribute
---

# How to harmonise a study

This guide explains how to take a study through a Harmonise run: extract its files, review what was extracted, transform it to a template, review the result, and export it into ODM. At each review you either approve the attempt or request changes to it. For what phases, attempts and reviews are, see [About Harmonise](about-harmonise.md#phases-attempts-and-review).

## Prerequisites

- Membership of the **Curator** group.
- LLM credentials for a provider that uses the OpenAI API, saved on your Profile page. Transform needs one: with another provider, the transform fails. Extract works without one, but then reads the files by their names and ignores the comments you make when you request changes. See [Save your LLM credentials](save-your-llm-credentials.md#which-provider-to-choose).
- The study's raw files in a folder of the S3 storage your ODM instance is set up with.
- An open run that is `READY`. See [Start and finish a run](start-and-finish-a-run.md#start-a-run).

The run takes one phase at a time: while an attempt is in progress, the run takes no other phase until it ends. Each attempt can take several minutes, as the run calls the LLM many times.

## Extract the files

1. On the run's page, enter the path of the folder that holds the study's files and click **List files**.
2. Check the listing, then click **Extract this folder**. The run page shows the attempt, `extract-1`, while it runs.
3. Wait until the attempt has `SUCCEEDED`. Its review then shows every file of the folder and how it was read, the objects extracted from the files, such as samples, and the findings, the problems the run noticed.

If the attempt `FAILED`, the run page shows why. Start the extraction again.

## Review the extraction

Read the attempt's review, then do one of the following:

- **The extraction is right.** Click **Approve and transform**, check the template to harmonise to, `public_studies` by default, and confirm. This starts the transformation; see [Transform the extraction](#transform-the-extraction).
- **Something is wrong.** Click **Request changes** and write your comments, one per row. Each row has a **Comment** and an optional context, what the comment is about; clicking **Comment** beside a file, a read, an object or a field of the review fills the context in for you. Leave the context empty for a comment on the whole attempt. Then click **Rerun extract with these comments**. The run extracts the same folder again, as a new attempt, `extract-2`, that takes your comments into account. Review that attempt in turn.

You can request changes as often as you need. Each new attempt revises the previous one, and once it succeeds, the previous one is marked **Superseded**.

!!! note
    Requesting changes to an extraction needs a provider that uses the OpenAI API. With another provider, the new attempt reads the files by their names again and does not use your comments: its review says *Feedback was not used, as no model is configured*.

## Transform the extraction

The transformation plans how the extracted data maps to the template's fields, carries out the plan, and checks the result, all in one attempt.

1. Wait until the attempt, `transform-1`, has `SUCCEEDED`. Its review shows the plan, how it ran, the entities it produced, where each field's values come from, and the findings.
2. Read the review, then do one of the following:
    - **The transformation is right.** Click **Approve and export**. This starts the export; see [Export into ODM](#export-into-odm).
    - **Something is wrong.** Click **Request changes**, write your comments, for example on a field such as `Sample.Disease`, and click **Rerun transform with these comments**. The run plans the transformation again, as a new attempt on the same extraction and template, then carries out and checks the new plan.

A plan that is not valid, or that could not be carried out, still comes to review, with findings that say what went wrong: request changes to it.

Once a transformation has succeeded, the run takes no more extractions: the extraction you approved is final for the run. To extract the files again, finish the run and start a new one.

## Export into ODM

The export writes the harmonised study, as a package of files, to the storage, under `harmonisation/runs/<run number>/<step>/`, and imports its study and samples into ODM as you, linked to each other.

1. Wait until the attempt, `export-1`, has `SUCCEEDED`. The run page shows the **Study** and the **Samples** it imported, by accession, and the **Package**: where it was written, `s3://<bucket>/harmonisation/runs/<run number>/export-1/`, and how many files it has.
2. Open the study in ODM to check it.

The export does not import expression data.

Once the export has succeeded, the run takes no more phases: a second export would import the study again.

If the export `FAILED`, the run page shows why, and you can export the same transformation again. But an export that failed part-way may have imported the study, and perhaps the samples, already: its error then names them, for example *Import into ODM failed: … (imported before it: study GSF…)*. Before you export again, find what it names in ODM and delete it, or the new export imports a second study.

## Finish the run

Click **Finish run** once the export has succeeded, or once you are done with it: see [Finish a run](start-and-finish-a-run.md#finish-a-run). The run's attempts, reviews and your comments stay on its page for good.

## Superseded attempts

An attempt is superseded once a later attempt of the same phase has succeeded. A superseded attempt stays on the run page, marked **Superseded**, with its review and the comments made on it, but you can no longer approve it or request changes to it: only the latest successful attempt of a phase can be reviewed.

An attempt that fails changes nothing: the attempt before it is still the one under review, and you can approve it or request changes to it again.

## Related

- [About Harmonise](about-harmonise.md#phases-attempts-and-review), what phases, attempts and reviews are.
- [Save your LLM credentials](save-your-llm-credentials.md), the credentials the phases call the LLM with.
- [How to run Harmonise via the API](../../odm-api/contribute/harmonise/how-to-run-harmonise-via-the-api.md), the same phases through the API.
