---
title: Config contract consistency
description: 'Apply a “configuration as a contract” standard: when behavior depends
  on environment/profile/feature flags (remote vs local, active management profile,
  accessibility mode, client/server timing), wire that configuration into *all* relevant
  code paths and keep its semantics consistent across layers.'
repository: nousresearch/hermes-agent
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 221948
---

Apply a “configuration as a contract” standard: when behavior depends on environment/profile/feature flags (remote vs local, active management profile, accessibility mode, client/server timing), wire that configuration into *all* relevant code paths and keep its semantics consistent across layers.

Checklist
- **Cover transitions, not just initial state:** if a feature flag can change at runtime (e.g., local→remote), ensure existing watchers/listeners and previously constructed components are updated or torn down accordingly.
- **Mirror configuration across sibling components:** if an option (e.g., `screenReaderMode`) is required for a user-facing terminal, ensure equivalent terminal variants (e.g., agent/output terminals with independent constructors) receive the same option.
- **Register every new config-dependent API endpoint:** when profile scoping is implemented via prefixes/lists, add new endpoints to the correct scoping registry so requests get the active profile.
- **Align client timeouts and docs with server caps:** do not set client ceilings/timeout comments that contradict the server’s actual maximum behavior.

Example patterns
- Profile-scoped endpoint registration:
```ts
// In api.ts / shared config
PROFILE_SCOPED_PREFIXES.add('/api/messaging/weixin/onboarding')
// so fetchJSON can append the active management profile
```
- Remote-aware watcher lifecycle (conceptual): on mode change, stop the local watcher and prevent reloading local disk plugins from existing callbacks.
- Consistent terminal options:
```ts
// In both terminal constructors
const termOptions = { /* ... */ screenReaderMode: true }
```
- Timeout semantics:
```ts
// Ensure client timeout constants/comments reflect the server’s real cap
export const PROFILES_REQUEST_TIMEOUT_MS = SERVER_CAP_MS // or remove misleading comments
```