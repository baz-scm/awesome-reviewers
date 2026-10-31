---
title: Document configuration overrides
description: When code silently overrides or hardcodes a value that a caller or owner
  could reasonably expect to control (e.g. forcing `target.persistent_memory = False`
  on every served request even though the agent was explicitly configured with `persistent_memory=True`),
  don't bury the rationale only in the PR description. Either expose the behavior
  as an explicit,...
repository: kyegomez/swarms#pi240310
label: Configurations
language: Python
comments_count: 3
repository_stars: 7337
---

When code silently overrides or hardcodes a value that a caller or owner could reasonably expect to control (e.g. forcing `target.persistent_memory = False` on every served request even though the agent was explicitly configured with `persistent_memory=True`), don't bury the rationale only in the PR description. Either expose the behavior as an explicit, documented configuration option (e.g. a constructor flag on `MCPDeployer`) so it's a deliberate, discoverable choice, or at minimum add an inline comment at the override site explaining why the setting is being forced and what the consequences are.

Similarly, when changing a configuration constant/threshold that gates behavior (e.g. `_BASH_MAX_LENGTH` controlling when commands get steered to `create_file` vs run directly), pick and justify the specific value in the PR/commit rather than an arbitrary multiplier ("raise the cap" is not "raise it 8x to 4096"). State what boundary behavior the new value is meant to produce, and keep tests pinned to concrete, fixed inputs that exercise both sides of the threshold rather than deriving test inputs from the constant itself — tests that scale with the constant they're supposed to validate no longer catch regressions if the constant changes unexpectedly.

Example of what to avoid:
```python
# No comment, no config flag — silently diverges from the agent's declared setup
target.persistent_memory = False
```
Prefer:
```python
# Served requests must not read or write MEMORY.md: it would leak one
# client's turns into another's prompt and accumulate indefinitely.
# Controlled by MCPDeployer(disable_persistent_memory=True), default True.
target.persistent_memory = self.disable_persistent_memory
```