<!--
Thanks for contributing! Please confirm the following before submitting.
-->

## What does this PR change?

<!-- Briefly describe what changed and why. e.g. "Add skill X with verified compatibility across 5 agents" -->

## Checklist

- [ ] `python scripts/validate.py` passes locally
- [ ] If I added/changed a skill, the `compatibility` and `caveats` fields are filled for every affected agent
- [ ] If I added a new agent, I also ran `python scripts/generate_agent_docs.py` and updated every skill's `compatibility` map
- [ ] I did **not** edit the README tables by hand (CI regenerates them)
- [ ] `verified_at` and `verified_by` are set for any new/updated skill cell

## Verification notes

<!-- How did you verify the cells you set? (installed, triggered, exercised a task, etc.) -->
