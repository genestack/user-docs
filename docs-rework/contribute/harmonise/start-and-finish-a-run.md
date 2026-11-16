---
diataxis: how-to
tab: contribute
---

# How to start and finish a run

This guide explains how to start a Harmonise run, how to finish it, and how to find it again once it is over. For what a run is and the states it goes through, see [About Harmonise](about-harmonise.md) and [Run lifecycle](run-lifecycle.md).

## Prerequisites

- Membership of the **Curator** group.
- LLM credentials that ODM can use, saved on your Profile page. See [Save your LLM credentials](save-your-llm-credentials.md).

## Start a run

1. Click the three-line menu at the top left of the Dashboard and select **Harmonise**. The page lists every run you started, by dataset folder: see [Find a run again](#find-a-run-again).
2. Click **New run**. The **New run** dialog opens.
3. In **Dataset folder**, enter the path of the folder that holds the study's files, within the run's bucket, for example `harmonisation-demo/GSE266358`.
4. Click **Start run**. The new run's page opens.
5. Wait while the run is `PENDING`: ODM is setting up its processing environment. Once the run is `READY`, it extracts the folder by itself, as its first attempt, `extract-1`.

**Start run** stays disabled until you enter a folder. If **New run** is disabled, point at it to see why. Usually it is because you have no LLM credentials ODM can use: follow the link to your Profile page and save them.

If the run refuses the extraction, the run page says why, and the folder stays entered in its **Extract** form: correct it and click **Extract**. If you leave the run's page before the run is `READY`, the extraction may not start: enter the folder in the **Extract** form then.

Between its start and its finish, the run takes a study through its phases: see [How to harmonise a study](harmonise-a-study.md).

## Finish a run

Finish a run once you are done with it. An open run keeps its processing environment, and fails when it reaches its time limit (see [Run lifecycle](run-lifecycle.md#time-limit)).

1. Open the run: select **Harmonise** in the three-line menu and click the run in the list.
2. Click **Finish run**. The run is `FINISHING`: the step in progress runs to its end, the steps that have not started are skipped, and the run shuts down.
3. Wait until the run is `FINISHED`. The page shows when it finished.

There is no cancel action: finishing a run is the only way to end it, and a step in progress always runs to its end. The Harmonise page lists a run that you finished before it imported a study as **Cancelled**.

## Find a run again

The Harmonise page lists every run you started, those that are over included. Runs are never deleted: click any row to open the run's page, with its steps and their results as they were, every attempt and its review included.

The list groups runs by dataset folder, the folder that the run's latest extraction named. Each group shows the folder's name, its location, such as `s3://<bucket>/harmonisation-demo/GSE266358`, and how many runs it has. The group with the newest run comes first, and runs are newest first within a group. Runs that have not named a folder yet are in the last group, **No folder named yet**. A group shows its 6 newest runs: click **Show N more runs** for the others, and **Show fewer runs** to hide them again.

Each run shows the following:

| Column | What it shows |
| --- | --- |
| Run ID | The run's number, for example *Run 42*. |
| Study Description | A dash, for now. |
| Stage | Three segments, one per phase: **Files read**, **Transformed** and **Imported**. A label says where the run is: *Now: …* while it works, *Waiting at: …* while it waits for you, *Stopped at: …* once it ended without an import, and *Imported* once it imported a study. |
| Status | Where the run stands, in five statuses: see the table below. Point at a status to see why the run has it. |
| Decisions | *1 decision required* while the run waits for you, *All clear* otherwise, and a dash for a run that is **Failed** or **Cancelled**. |
| Author | Who started the run. |
| Started | When the run started. |

The list reads a run's status from its state and its steps:

| Status | Meaning |
| --- | --- |
| In progress | The run is `PENDING`, or a step is waiting for its turn or in progress. |
| Waiting for human | The run is `READY` and waits for your next step: name a folder to extract, review the latest attempt, or try again after a failed attempt. |
| Imported | An export succeeded, or an upload to ODM succeeded and no extract, transform or export step came after it: the study is in ODM. The run may still be open, or have failed after the import. Finish an open run once you are done with it. |
| Failed | The run is `FAILED`, without an import. |
| Cancelled | You finished the run, which is `FINISHING` or `FINISHED`, without an import. |

For the states behind these statuses, see [Run lifecycle](run-lifecycle.md#states).

## Related

- [Run lifecycle](run-lifecycle.md), the states a run goes through and why a run fails.
- [How to harmonise a study](harmonise-a-study.md), what to do with a run once it is ready.
- [Save your LLM credentials](save-your-llm-credentials.md), the credentials a run needs to start.
- [How to run Harmonise via the API](../../odm-api/contribute/harmonise/how-to-run-harmonise-via-the-api.md), the same steps through the API.
