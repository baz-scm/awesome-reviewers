---
title: Config Scope And Hygiene
description: 'Treat configuration as a product surface: make it correct, discoverable,
  and safe.


  Practical rules:

  1) Document scope/precedence explicitly: If an override is ineffective for certain
  commands due to caching/initialization order, state that clearly and point users
  to the effective setting (global config or env var).'
repository: the-pr-agent/pr-agent
label: Configurations
language: Toml
comments_count: 7
repository_stars: 12523
---

Treat configuration as a product surface: make it correct, discoverable, and safe.

Practical rules:
1) Document scope/precedence explicitly: If an override is ineffective for certain commands due to caching/initialization order, state that clearly and point users to the effective setting (global config or env var).
2) Keep one source of truth: Don’t mirror flags in a repo’s active `.pr_agent.toml` when the canonical flag and docs live in `configuration.toml`/docs; only override when you can guarantee intended behavior.
3) Avoid dead or misleading toggles: Don’t add/retain “exotic” flags with defaults that imply unused behavior. If the intended product behavior is “always skip drafts,” prefer making the toggle unnecessary (or align the default with real usage without breaking changes).
4) Improve config ergonomics: Namespace/group related “incremental” options instead of a long flat list; move large optional feature blocks (e.g., custom labels) to dedicated optional config files.
5) Guard incompatible settings: If two flags can cause contradictory behavior (edit vs create/delete, update vs delete), add validation, warnings, or tests; prefer mechanisms that preserve traceability when appropriate.
6) Separate secrets from shared config: tokens/auth belong in user-provided secrets files (e.g., per-user `*.secrets.toml`), not in versioned or global configuration.

Example (scope documentation pattern):
```toml
# Optional base URL used to build links in user-facing comments.
# Note: per-repo overrides may not apply to /describe, /review, /improve
# because the provider is constructed/cached before repo settings are merged.
# Recommended: set globally or via env var.
# web_url = ""
```