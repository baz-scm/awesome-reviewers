---
title: Centralize config resolution
description: 'Configuration values (remote/branch selection, feature-flag checks,
  disabled/enabled markers, provider IDs, environment/base-URL, host info) must be
  resolved by one shared function and reused everywhere, not re-implemented or re-read
  ad hoc in each call site. Divergent logic for the "same" setting is a recurring
  source of bugs: a handoff tool picking a...'
repository: 'cline/cline

  '
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70942
---

Configuration values (remote/branch selection, feature-flag checks, disabled/enabled markers, provider IDs, environment/base-URL, host info) must be resolved by one shared function and reused everywhere, not re-implemented or re-read ad hoc in each call site. Divergent logic for the "same" setting is a recurring source of bugs: a handoff tool picking a different Git remote than the workspace manifest, a skill installer's hand-rolled frontmatter parser accepting/rejecting different skills than the actual loader, an `isFrontmatterDisabled` check that didn't match the loader's precedence rules, and a provider-ID lowercasing that caused save/delete to target a different settings key than lookup (`nousResearch` vs `nousresearch`), silently leaving providers unconfigured or credentials un-deleted.

Likewise, business logic should consult the config value through the same authoritative check used elsewhere (e.g. checkpoint availability should use the same per-run rule as restore, not independently re-check the global "enable checkpoints" setting), and values that are fixed for the process lifetime (app base URL, backend environment, host name) should be resolved once at startup and passed/cached, rather than re-read from provider settings or via an IPC/host-bridge call on every request.

When adding or changing configuration reads:
- Extract the resolution/normalization logic into a single shared function and call it from every place that needs the value (save, load, delete, display).
- Normalize keys/IDs consistently (e.g. don't lowercase on write if the canonical ID is mixed-case) so writes and reads target the same entry.
- For values that cannot change during the process lifetime, resolve once at startup and inject/cache the result instead of re-fetching per call.
- When a setting can be toggled independently of a specific resource's state (e.g. "enable checkpoints" vs "does this checkpoint exist"), check the narrower, resource-specific state rather than the broader toggle, so an existing resource/config isn't hidden by an unrelated setting change.

Example of the normalization bug to avoid:
```ts
// Built-in provider id is "nousResearch"
const providerId = request.providerId.trim().toLowerCase(); // -> "nousresearch"
// Save/delete now target a different key than lookup uses ("nousResearch"),
// so saving leaves the provider unconfigured and "disabling" an existing
// config reports success while leaving credentials in place.
```