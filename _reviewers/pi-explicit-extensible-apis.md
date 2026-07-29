---
title: Explicit, Extensible APIs
description: When designing/adjusting API surfaces, ensure (1) consumers can clearly
  understand what they’re setting and what defaults apply, (2) implementation-only
  details don’t leak into public types, and (3) variant-specific behavior is routed
  through dedicated abstractions/resolvers rather than embedded special-cases.
repository: earendil-works/pi
label: API
language: TypeScript
comments_count: 4
repository_stars: 79783
---

When designing/adjusting API surfaces, ensure (1) consumers can clearly understand what they’re setting and what defaults apply, (2) implementation-only details don’t leak into public types, and (3) variant-specific behavior is routed through dedicated abstractions/resolvers rather than embedded special-cases.

Guidelines:
- Don’t expose “internal” fields in public types. If it’s truly a public concept, make it a public argument and define whether it’s optional and its default.
- If you use an options object to reduce argument count, make callsites unambiguous. Prefer patterns that make usage explicit (e.g., explicit option properties at callsites, or split into multiple functions when most options are unused).
- Centralize provider/variant-specific logic (e.g., base URL resolution) behind a single resolver/adapter so adding new variants doesn’t grow conditional branching in core flows.
- Prefer higher-level abstractions for behavioral APIs. If string lists/primitive inputs lead to unintended behavior (like terminal wrapping), switch to a component/object-based interface that captures rendering intent.

Example (options + explicit defaults + no internal leakage):
```ts
export interface AgentSessionOptions {
  source?: "interactive" | "rpc" | "extension"; // public, documented
}

export function createAgentSession(opts: AgentSessionOptions = {}) {
  const source = opts.source ?? "interactive";
  // ...
}

// Avoid embedding provider-specific branching in unrelated call paths:
function resolveBaseUrl(model: { provider: string; baseUrl: string }) {
  if (model.provider === "cloudflare") return resolveCloudflareBaseUrl(model);
  return model.baseUrl;
}
```

Apply this checklist whenever you modify exported types, request/response shapes, client interfaces, or any public function signatures that other teams/code depends on.