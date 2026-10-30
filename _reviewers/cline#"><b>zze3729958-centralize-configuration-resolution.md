---
title: Centralize configuration resolution
description: 'Environment- and settings-derived values (base URLs, host metadata,
  feature-enablement rules, telemetry gates) must be resolved from a single canonical
  function or module, not re-implemented or re-derived independently in each consumer.
  Duplicated resolution logic drifts out of sync and causes real bugs: a staging provider
  override opened the production app...'
repository: cline/cline#"><b>zze3729958
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 71067
---

Environment- and settings-derived values (base URLs, host metadata, feature-enablement rules, telemetry gates) must be resolved from a single canonical function or module, not re-implemented or re-derived independently in each consumer. Duplicated resolution logic drifts out of sync and causes real bugs: a staging provider override opened the production app because one code path used the resolved backend URL while another used `getClineEnvironmentConfig().appBaseUrl`; an extension's own copy of the "is this rule disabled" logic repeatedly diverged from the SDK's parser; host name and telemetry settings were being fetched or gated differently depending on the code path.

To apply this:
- Resolve environment/config-dependent values once, ideally at startup, and store/pass the resolved value down (e.g. `ctx.clineAppBaseUrl` set once from `resolveSidecarClineAppBaseUrl()`, or `HostRegistryInfo` populated once before any state is built) rather than re-querying providers or making bridge calls on every request.
- When the same semantic value is needed in multiple runtimes or packages (CLI, desktop sidecar, extension, SDK), extract one shared helper (e.g. `resolveClineAppBaseUrl(apiBaseUrl)` in `@cline/shared`, `parseRuleConfigFromMarkdown`/`parseSkillConfigFromMarkdown` in `@cline/core`) and have every consumer call it, instead of hand-rolling an equivalent parser or lookup.
- If an input can't be mapped to a known environment/config (e.g. a proxy or self-hosted backend with no matching app URL), resolve to an explicit "unknown" state and have callers hide/disable the dependent feature rather than silently falling back to a different environment.
- When unifying previously-divergent config gates (e.g. two telemetry policy pipelines), keep behavior-neutral unless you explicitly decide to change semantics, and track any intended follow-up unification separately.

Example:
```ts
// Bad: each caller re-derives the app URL from different sources
const url = providerSettings.baseUrl ?? getClineEnvironmentConfig().appBaseUrl;

// Good: resolve once from the actual backend being used, shared everywhere
const appBaseUrl = resolveClineAppBaseUrl(resolvedAccountApiBaseUrl); // undefined if backend is unrecognized
```
