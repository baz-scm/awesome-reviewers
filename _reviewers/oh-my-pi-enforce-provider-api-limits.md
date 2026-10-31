---
title: Enforce provider API limits
description: When mapping internal config or settings onto a third-party provider's
  wire format, validate against that provider's actual documented constraints instead
  of forwarding values unbounded or assuming a capability only applies when it is
  explicitly advertised. Silently passing through an over-limit value (too many array
  entries, a too-long identifier, an...
repository: can1357/oh-my-pi
label: API
language: TypeScript
comments_count: 3
repository_stars: 37317
---

When mapping internal config or settings onto a third-party provider's wire format, validate against that provider's actual documented constraints instead of forwarding values unbounded or assuming a capability only applies when it is explicitly advertised. Silently passing through an over-limit value (too many array entries, a too-long identifier, an unsupported enum value) causes the provider to reject the entire request, which is worse than degrading gracefully. Concretely:
- Identify the hard limit from the provider's docs or reference implementation (e.g., Anthropic's `fallbacks` array accepts at most 3 entries; Meta Responses tool names must be ≤64 characters).
- Cap, truncate, or reject input that would exceed the limit, and make the behavior explicit and observable — log a warning when truncating, or throw a clear configuration error, and add a regression test that pins the boundary.
- Don't infer provider capability purely from a discovery/catalog response if the reference client treats a parameter as always request-able (e.g., Anthropic `service_tier: "flex"` is a valid request option even when not listed in discovery); verify with real provider behavior before removing an existing exemption.

Example (capping instead of blind pass-through):
```ts
const ANTHROPIC_MAX_FALLBACK_MODELS = 3; // Anthropic wire limit

const configured = settings.get("providers.anthropic.serverSideFallbackModels").filter(id => id.trim());
if (configured.length > ANTHROPIC_MAX_FALLBACK_MODELS) {
  logger.warn(`Configured ${configured.length} fallback models; only the first ${ANTHROPIC_MAX_FALLBACK_MODELS} will be sent (Anthropic wire limit).`);
}
const fallbacks = configured.slice(0, ANTHROPIC_MAX_FALLBACK_MODELS).map(id => ({ model: id }));
```
Applying this consistently prevents requests from failing wholesale at the provider boundary and keeps the failure mode (if any) explicit and testable rather than a surprise 400 in production.