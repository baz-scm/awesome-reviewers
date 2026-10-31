---
title: Keep inline docs synchronized
description: 'Documentation that lives only in a PR description is invisible to anyone
  reading the code later; it must be captured where future readers will actually see
  it — in docstrings and comments attached to the code itself. Two failure modes to
  avoid:'
repository: kyegomez/swarms#pi240310
label: Documentation
language: Python
comments_count: 4
repository_stars: 7337
---

Documentation that lives only in a PR description is invisible to anyone reading the code later; it must be captured where future readers will actually see it — in docstrings and comments attached to the code itself. Two failure modes to avoid:

1. **Undocumented limitations/behavior.** When a public method has a non-obvious scope or caveat (e.g. `to_dict(strict=True)` only guarantees faithfulness for `SerializableMixin` attributes, not for nested objects with their own unrelated `to_dict()` implementations such as `Conversation` or `GraphWorkflow`), state that limitation in the method's docstring `Args`/`Returns`/`Notes` section. Relying on "it's explained in the PR body" leaves every future caller to rediscover the gap the hard way. Likewise, if a piece of code is intentionally kept despite looking dead or unused (e.g. an audit-log accessor with no current callers), add a short comment/docstring note explaining why it's retained, so it isn't deleted by a future cleanup pass.

2. **Stale comments.** When code under a comment header is removed or relocated, update or delete the comment too. Leaving a header like `# System shutdown / reboot` with no entries beneath it (because the checks moved into `_BASH_COMMAND_WORDS`) misleads the next reader into thinking that case isn't covered at all.

Example:
```python
def to_dict(self, strict: bool = False) -> dict:
    """
    Serialize this object to a dict.

    Args:
        strict: If True, raise instead of emitting a placeholder for
            non-serializable values found on this object or in nested
            SerializableMixin attributes. NOTE: strict is NOT forwarded
            to attributes whose class defines its own to_dict() (e.g.
            Conversation, MCPManager, GraphWorkflow); their output is not
            covered by this guarantee.
    """
```

Before merging, check that any new behavior/limitation/design rationale is documented in-code (docstring or comment), and that any comments referencing removed/moved code are updated or removed in the same change.</description>
</invoke>
