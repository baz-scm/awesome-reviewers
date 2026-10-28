---
title: Document only verified behavior
description: 'Documentation should describe exactly what the product currently does,
  not what it used to do, what it''s supposed to do, or what a maintainer assumes
  it does. Before publishing, verify each claim and example against the actual implementation:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Documentation
language: Other
comments_count: 7
repository_stars: 70964
---

Documentation should describe exactly what the product currently does, not what it used to do, what it's supposed to do, or what a maintainer assumes it does. Before publishing, verify each claim and example against the actual implementation:

- If a feature is deprecated, removed, or no longer functional, remove its documentation rather than describing it as "broken" or "has no effect." Documenting a dead option (e.g. a config var that silently does nothing) invites users to rely on it and looks confusing; either fix the product or delete the docs, and only keep a "known caveat" note when the fix is actively planned and non-trivial.
- Test every command/example exactly as written. For instance, `cline connect telegram --restart -k <TOKEN>` only works if the option comes before the subcommand that consumes the rest of the arguments — verify argument order and flag behavior rather than assuming it mirrors a similar command.
- Avoid overstating guarantees or completeness. Prefer precise, falsifiable wording ("the CLI *supports* X" vs. "the CLI *enforces* X") and don't imply a list or table is exhaustive unless it truly is — instead explain the general rule or class of behavior so readers can reason about cases not explicitly listed.
- Double check "does X" claims against edge cases (e.g., "waits for the hub to go idle" should specify which kinds of running work it does/doesn't wait for) so the doc doesn't silently mislead users for less common workflows.

Treating documentation as a contract that must match the current, tested behavior of the system — not a historical or aspirational record — keeps the docs trustworthy and reduces support burden from misled users.</description>
</invoke>
