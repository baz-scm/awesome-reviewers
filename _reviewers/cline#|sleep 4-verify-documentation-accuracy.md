---
title: Verify documentation accuracy
description: 'Documentation must precisely reflect the product''s current, actual
  behavior. Before publishing:


  - Test every command, code snippet, and config example exactly as written to confirm
  it works (e.g., verify flag ordering like `cline connect telegram --restart -k <BOT-TOKEN>`
  actually reaches the connector, not just that it parses).'
repository: cline/cline#|sleep 4
label: Documentation
language: Other
comments_count: 7
repository_stars: 70979
---

Documentation must precisely reflect the product's current, actual behavior. Before publishing:

- Test every command, code snippet, and config example exactly as written to confirm it works (e.g., verify flag ordering like `cline connect telegram --restart -k <BOT-TOKEN>` actually reaches the connector, not just that it parses).
- Never document a feature, flag, or setting that is broken, removed, or has no effect. If something no longer works (like `CLINE_HOOKS_DIR` or a deprecated `.clineignore` filter), either fix the underlying behavior or delete the documentation—don't leave a row/section describing something that silently does nothing, since that erodes trust in the rest of the docs.
- Use verbs and claims that match the real guarantee. Don't say a feature "enforces" a rule if it only "supports" or "applies" it by default and can be overridden; don't imply a list of values is exhaustive if new values can appear—instead tell readers to gracefully ignore types/fields they don't recognize.
- Keep platform- or build-specific details consistent across all variants (e.g., stable vs. nightly key prefixes), and account for each in your examples rather than assuming a single build.
- When writing step-by-step UI instructions, order them to match the actual navigation path the user follows (e.g., "go to Features → Advanced → turn on Hooks", not an order that requires jumping backward through the UI).

Treat the moment you update docs as an opportunity to validate the feature's real state, and prefer removing or fixing stale/incorrect content over leaving vague caveats, unless the fix is large enough to require a tracked follow-up.</description>
</invoke>
