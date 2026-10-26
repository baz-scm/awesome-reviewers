---
title: Verify docs against actual behavior
description: 'Documentation (CLI references, config tables, examples) must accurately
  reflect the current, real behavior of the system—not assumed, aspirational, or stale
  behavior. Before merging docs:'
repository: cline/cline
label: Documentation
language: Other
comments_count: 5
repository_stars: 70886
---

Documentation (CLI references, config tables, examples) must accurately reflect the current, real behavior of the system—not assumed, aspirational, or stale behavior. Before merging docs:

1. Test every example/command as written to confirm it actually works (e.g., option ordering, flags). If an example is wrong—like putting `--restart`/`--stop` after the channel name when the parser only forwards trailing args to the channel—fix the example and explain why ordering matters.
2. Cross-check documented defaults and behavior against the actual source/help output, not memory or intent. If code says `args.retries ?? 3` but docs say the default is `6`, the docs are wrong and must be corrected to match the code.
3. Never document a broken or non-functional feature as if it works normally. If something like an env var or flag is dead code, either fix the underlying functionality so the doc is true, or remove the documentation entirely. Avoid vague "accepted but ignored" wording, since it invites users to rely on something that silently does nothing.
4. Account for environment/build variants (e.g., nightly vs. stable channels, feature flags) that change the documented behavior, and make this explicit in the text so instructions don't silently fail for a subset of readers.

When in doubt, treat the actual `--help` output, running code, or manifest logic as the source of truth, and update prose/tables to match it exactly.