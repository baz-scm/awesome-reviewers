---
title: Provider capability handling
description: 'LLM provider integrations must reflect each provider''s actual behavior
  rather than assuming a uniform, "portable" abstraction works everywhere. Before
  forwarding a feature or computing a budget, verify what the specific provider/model
  combination actually supports and reports:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70964
---

LLM provider integrations must reflect each provider's actual behavior rather than assuming a uniform, "portable" abstraction works everywhere. Before forwarding a feature or computing a budget, verify what the specific provider/model combination actually supports and reports:

- Context/token limits: use the value that reflects what is actually being served, not just the advertised ceiling. For example, LM Studio reports both `max_context_length` (the model's max) and `loaded_context_length` (what's actually served, which can be much smaller); using the ceiling for compaction budgets lets requests exceed what the server will accept.
- Feature support (e.g. reasoning/thinking options): don't forward a portable option to a provider/model that can't translate it safely. Gate it with an explicit capability check (e.g. "does the catalog advertise reasoning controls for this model?") instead of relying on an incidental short-circuit elsewhere in the call path, and require callers to pass that context explicitly so it can't be silently skipped.
- Usage/accounting shapes: providers report fields like reasoning tokens inconsistently (sometimes nested under `outputTokens.reasoning`, sometimes as a sibling field, sometimes as a true subset of `outputTokens`). Normalize these explicitly and add a path/table for each known shape so reasoning tokens are never double-counted (once in their own field and again inside output tokens) or dropped by downstream consumers (session totals, telemetry, billing).
- Narrow, documented special cases: when a provider needs bespoke handling (e.g. Bedrock's Converse API rejecting `reasoningConfig` for non-reasoning models), keep the logic as small and explicit as possible, document why it's needed and which upstream issue it tracks, and prefer fixing the root cause in the shared adapter/SDK over accumulating provider-specific branches. Back these paths with wire-level tests that assert on the actual request/response the adapter produces, and keep test comments/PR descriptions precise about what is and isn't covered (e.g. whether a case still depends on catalog-based model resolution).

Example pattern for gating a feature by capability rather than provider name alone:

```ts
function modelAdvertisesReasoning(modelId: string, catalog: ModelCatalog): boolean {
  return catalog.getReasoningControls(modelId) !== undefined;
}

if (modelAdvertisesReasoning(request.modelId, catalog)) {
  providerOptions.reasoning = resolvePortableReasoning(request, context);
}
```

Applying this discipline prevents silent failures like premature truncation from stale context limits, malformed requests from unsupported options, and incorrect cost/usage telemetry from misclassified token counts.