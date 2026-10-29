---
title: Verify docs match behavior
description: 'Documentation must describe what the product actually does today, not
  what it used to do, what it was planned to do, or what a line of code implies it
  should do. Before merging a doc change, verify every claim and example against the
  current implementation:'
repository: cline/cline#1
label: Documentation
language: Other
comments_count: 6
repository_stars: 71024
---

Documentation must describe what the product actually does today, not what it used to do, what it was planned to do, or what a line of code implies it should do. Before merging a doc change, verify every claim and example against the current implementation:

- Don't document dead or non-functional features. If `.clineignore` or a flag like `CLINE_HOOKS_DIR` no longer has any effect, either fix the underlying code so it works again, or delete the feature and its documentation entirely. A page that says "this does nothing" is a sign the feature (and its doc) should be removed, not caveated indefinitely.
- Test every CLI/code example before publishing it. The `cline connect telegram --restart -k <TOKEN>` example looked plausible but failed because the flag parser requires options before the channel argument — the kind of bug only caught by actually running the example.
- Avoid overclaiming capability. Prefer precise verbs: a product that reads config into a session but lets the user edit it afterward "supports" a control, it does not "enforce" it.
- Keep reference tables honest about scope. If a table only lists event/message types that scripts need to parse, say so explicitly rather than implying it enumerates every possible value, and omit internal/status-only types that add noise without actionable value.
- When a setting or feature behaves differently across build variants (e.g., stable vs. nightly, legacy vs. next), confirm the doc's instructions (such as a settings key name) actually apply to all variants mentioned, not just the primary one.

Treat inaccurate or stale documentation as a bug: fix the product to match the docs, or fix the docs to match the product — never leave both diverging.