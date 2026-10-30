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

1. Click the three-line menu at the top left of the Dashboard and select **Harmonise**. The page lists every run you started, newest first.
2. Click **Start run**. The new run's page opens.
3. Wait while the run is `PENDING`: ODM is setting up its processing environment. Once the run is `READY`, it takes the steps you ask for on its page.

If **Start run** is disabled, point at it to see why. Usually it is because you have no LLM credentials ODM can use: follow the link to your Profile page and save them.

!!! note
    The steps a run offers between its start and its finish are early versions and will change as Harmonise develops. The run page shows the ones available now.

## Finish a run

Finish a run once you are done with it. An open run keeps its processing environment, and fails when it reaches its time limit (see [Run lifecycle](run-lifecycle.md#time-limit)).

1. Open the run: select **Harmonise** in the three-line menu and click the run in the list.
2. Click **Finish run**. The run is `FINISHING`: the step in progress runs to its end, the steps that have not started are skipped, and the run shuts down.
3. Wait until the run is `FINISHED`. The page shows when it finished.

A run cannot be cancelled: finishing it is the only way to end it, and a step in progress always runs to its end.

## Find a run again

The Harmonise page lists every run you started, those that are over included, newest first, with its number, status and times. Runs are never deleted: click any of them to see its steps and their results as they were.

## Related

- [Run lifecycle](run-lifecycle.md), the states a run goes through and why a run fails.
- [Save your LLM credentials](save-your-llm-credentials.md), the credentials a run needs to start.
- [How to run Harmonise via the API](../../odm-api/contribute/harmonise/how-to-run-harmonise-via-the-api.md), the same steps through the API.
