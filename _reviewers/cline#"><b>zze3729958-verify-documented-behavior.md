---
title: Verify documented behavior
description: Documentation must describe only behavior that actually exists in the
  current release, and every factual claim (commands, options, file paths, config
  keys) should be verified against the real source/runtime before it is published.
  Don't document a feature or flag as "broken" or "has no effect" just to preserve
  a historical reference — if a feature is...
repository: cline/cline#"><b>zze3729958
label: Documentation
language: Other
comments_count: 6
repository_stars: 71067
---

Documentation must describe only behavior that actually exists in the current release, and every factual claim (commands, options, file paths, config keys) should be verified against the real source/runtime before it is published. Don't document a feature or flag as "broken" or "has no effect" just to preserve a historical reference — if a feature is non-functional, deprecated, or ignored, either fix it and keep the doc accurate, or remove the doc/feature entirely rather than leaving a confusing half-true entry that invites misuse. For example, prefer deleting a row like `| CLINE_HOOKS_DIR | Has no effect in this release |` over keeping it, and drop options/flags that are silently ignored (e.g., removing a `--limit` row that implied functionality that wasn't there) rather than documenting them as "accepted but ignored." When something is genuinely transitional (e.g., a large fix is in progress and can't land immediately), it's acceptable to note the caveat explicitly and track the follow-up work, but this should be the exception, not the default. Before writing examples or troubleshooting steps, confirm they work as described — check actual argument parsing (e.g., option placement for `cline connect telegram --restart -k <TOKEN>`) and trace real file writers/paths (e.g., using `lsof` or reading source to confirm which log file a given client actually writes, rather than reusing an assumption). When documenting behavior that varies by provider, backend, or environment, be explicit about the boundary of that behavior and give practical, user-facing guidance for identifying which case applies, rather than a partial or non-exhaustive list; call out such caveats with clear visual emphasis (e.g., a dedicated "Note/Caveat" callout) so readers don't miss them.