---
diataxis: how-to
tab: contribute
---

# How to save your LLM credentials

Harmonise runs call a large language model (LLM) with your own API key. This guide explains how to save your credentials, a provider, a model and your key, on your Profile page, how to change them, and how to check that the provider accepts your key. You cannot start a run until you have saved credentials that ODM can use.

## Prerequisites

- Membership of the **Curator** group.
- An account with one of the LLM providers your ODM instance offers, and an API key for it. The providers and their models are set up by a user with the **Harmonisation Administrator** permission; see [Manage LLM providers](../../admin/manage-users/manage-llm-providers.md).

## Save your credentials

1. Click your username or email address in the top-right corner and select **Profile**.
2. Scroll to the last section, **LLM credentials for Harmonise**.
3. Choose a **Provider**, then one of its models in **Model**.
4. Paste your key for that provider into **API key**.
5. Click **Save**. The section reads *Key saved on* and the date.

ODM never shows your key again once it is saved, and it makes no call to the provider when you save: a key the provider would refuse is saved all the same. To find out whether the provider accepts it, check it with a run (see [Check your key](#check-your-key)).

A key is 1 to 1024 printable ASCII characters, without spaces.

## Change your credentials

- **Another model of the same provider:** choose it in **Model** and click **Save**, leaving **API key** empty. Your saved key stays.
- **A new key:** type it into **API key** and click **Save**.
- **Another provider:** choose it and its model, and type your key for that provider: another provider needs its own key.

Runs that have already started keep the credentials they started with. What you save applies to the runs you start afterwards.

## Delete your credentials

Click **Delete** in the section and confirm. You cannot start a run until you save credentials again. Runs that have already started keep the credentials they started with.

## When your credentials stop working

A Harmonisation Administrator can remove a provider, or one of its models, after you chose it. The section then says so:

- *Your provider is no longer offered: choose another*
- *Your model is no longer offered: choose another*

Until you choose again and save, you cannot start a run.

## Check your key

Saving your credentials does not tell you whether the provider accepts your key. An open run can check it: **Check LLM key** on the run's page asks the provider about your model, with the key the run started with. The check costs no tokens.

A failed check says why in a sentence, with the provider's answer, and links to your Profile page when saving new credentials can fix it. The most common causes:

| Meaning | What to do |
|---|---|
| The provider refused your key. | Check the key with your provider, save it again, and start a new run. |
| The provider does not know your model, or your key may not use it. | Choose a model your key may use, save, and start a new run. |
| The provider did not answer. | Try again later. If it persists, ask your administrator whether ODM can reach the provider. |
| No credentials were saved when the run started. | Save your credentials and start a new run. |

A check can also fail for another reason, such as an answer from the provider that ODM does not expect, or a provider address it cannot call. Its message then says why.

A run keeps the credentials it started with, so a key you fix applies to the next run, not to the run that found the problem.

## Related

- [About Harmonise](about-harmonise.md), how runs use your key.
- [Start and finish a run](start-and-finish-a-run.md), starting a run once your credentials are saved.
- [Manage LLM credentials via the API](../../odm-api/contribute/harmonise/manage-llm-credentials-via-the-api.md), the same operations through the API.
