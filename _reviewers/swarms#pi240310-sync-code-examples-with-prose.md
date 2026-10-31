---
title: Sync code examples with prose
description: When updating a code example in documentation, update the surrounding
  explanatory text and inline comments in the same change so they accurately describe
  the new code's behavior. Pay special attention to cases where a refactor removes
  an explicit parameter (e.g., `loops_per_agent`, `num_agents`) that the prose relies
  on, introduces implicit conventions...
repository: kyegomez/swarms#pi240310
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 7337
---

When updating a code example in documentation, update the surrounding explanatory text and inline comments in the same change so they accurately describe the new code's behavior. Pay special attention to cases where a refactor removes an explicit parameter (e.g., `loops_per_agent`, `num_agents`) that the prose relies on, introduces implicit conventions (e.g., inferring the judge from list position/order in `agents=[pro, con, judge]`), or adds a required-but-non-obvious setting that silently no-ops if omitted (e.g., `streaming_on=True` being needed for `streaming_callback` to fire). If a behavior depends on ordering, naming, or a hidden flag, add a short comment or sentence making that explicit, for example:

```python
# Agents must set streaming_on=True for streaming_callback to fire
agent = Agent(..., streaming_on=True)
```

Before merging a doc change, re-read the prose immediately above/below the snippet and confirm every claim still matches the code, and that any non-obvious requirement for the example to work is spelled out rather than left for the reader to discover by trial and error.