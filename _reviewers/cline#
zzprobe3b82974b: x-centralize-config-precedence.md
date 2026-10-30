---
title: Centralize config precedence
description: When a setting can come from more than one place — CLI flags, environment
  variables, persisted/saved settings, and built-in defaults — define one explicit
  precedence order and implement the resolution logic in a single shared function
  that every caller reuses, rather than re-deriving or re-checking it ad hoc in each
  consumer.
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 71067
---

When a setting can come from more than one place — CLI flags, environment variables, persisted/saved settings, and built-in defaults — define one explicit precedence order and implement the resolution logic in a single shared function that every caller reuses, rather than re-deriving or re-checking it ad hoc in each consumer.

Concretely:
- Document and enforce the order explicitly (e.g. CLI flag > env var > persisted setting > default). Don't trust a framework's convenience default (e.g. Commander defaulting a negatable `--no-mouse` to `true`) to stand in for "not set" — check `getOptionValueSource(...)` or an equivalent "was this explicitly provided" signal before falling back to env/persisted values, otherwise the fallback is silently clobbered.
- When a caller can override a derived default (e.g. `allowBindFallback`), make the caller-supplied value win and use the derived value only as the `??` fallback, never the other way around.
- If the same decision (e.g. "which base URL/environment is active", "which env var holds this provider's API key", "is extended thinking enabled") is needed in more than one place, extract it into one shared helper and have every site (CLI, extension, sidecar, hub, provider runtime) call that helper. Divergent, independently-reimplemented lookups are the recurring root cause of environment/URL mismatches and inconsistent env-var fallback behavior.
- Add regression tests for every combination of sources (flag set, flag unset with env set, neither set, both set with conflicting values) so precedence bugs are caught before release.

Example pattern to follow:
```ts
// Caller-supplied value always wins; derived value is only the fallback.
const allowBindFallback = options.allowBindFallback ?? !hasExplicitEndpoint;

// "Was this explicitly set" check, not the raw (possibly defaulted) option value.
const authMouse =
  (authCmd.getOptionValueSource("mouse") === "cli" ? authCmd.opts().mouse : undefined) ??
  (program.getOptionValueSource("mouse") === "cli" ? program.opts().mouse : undefined);
```