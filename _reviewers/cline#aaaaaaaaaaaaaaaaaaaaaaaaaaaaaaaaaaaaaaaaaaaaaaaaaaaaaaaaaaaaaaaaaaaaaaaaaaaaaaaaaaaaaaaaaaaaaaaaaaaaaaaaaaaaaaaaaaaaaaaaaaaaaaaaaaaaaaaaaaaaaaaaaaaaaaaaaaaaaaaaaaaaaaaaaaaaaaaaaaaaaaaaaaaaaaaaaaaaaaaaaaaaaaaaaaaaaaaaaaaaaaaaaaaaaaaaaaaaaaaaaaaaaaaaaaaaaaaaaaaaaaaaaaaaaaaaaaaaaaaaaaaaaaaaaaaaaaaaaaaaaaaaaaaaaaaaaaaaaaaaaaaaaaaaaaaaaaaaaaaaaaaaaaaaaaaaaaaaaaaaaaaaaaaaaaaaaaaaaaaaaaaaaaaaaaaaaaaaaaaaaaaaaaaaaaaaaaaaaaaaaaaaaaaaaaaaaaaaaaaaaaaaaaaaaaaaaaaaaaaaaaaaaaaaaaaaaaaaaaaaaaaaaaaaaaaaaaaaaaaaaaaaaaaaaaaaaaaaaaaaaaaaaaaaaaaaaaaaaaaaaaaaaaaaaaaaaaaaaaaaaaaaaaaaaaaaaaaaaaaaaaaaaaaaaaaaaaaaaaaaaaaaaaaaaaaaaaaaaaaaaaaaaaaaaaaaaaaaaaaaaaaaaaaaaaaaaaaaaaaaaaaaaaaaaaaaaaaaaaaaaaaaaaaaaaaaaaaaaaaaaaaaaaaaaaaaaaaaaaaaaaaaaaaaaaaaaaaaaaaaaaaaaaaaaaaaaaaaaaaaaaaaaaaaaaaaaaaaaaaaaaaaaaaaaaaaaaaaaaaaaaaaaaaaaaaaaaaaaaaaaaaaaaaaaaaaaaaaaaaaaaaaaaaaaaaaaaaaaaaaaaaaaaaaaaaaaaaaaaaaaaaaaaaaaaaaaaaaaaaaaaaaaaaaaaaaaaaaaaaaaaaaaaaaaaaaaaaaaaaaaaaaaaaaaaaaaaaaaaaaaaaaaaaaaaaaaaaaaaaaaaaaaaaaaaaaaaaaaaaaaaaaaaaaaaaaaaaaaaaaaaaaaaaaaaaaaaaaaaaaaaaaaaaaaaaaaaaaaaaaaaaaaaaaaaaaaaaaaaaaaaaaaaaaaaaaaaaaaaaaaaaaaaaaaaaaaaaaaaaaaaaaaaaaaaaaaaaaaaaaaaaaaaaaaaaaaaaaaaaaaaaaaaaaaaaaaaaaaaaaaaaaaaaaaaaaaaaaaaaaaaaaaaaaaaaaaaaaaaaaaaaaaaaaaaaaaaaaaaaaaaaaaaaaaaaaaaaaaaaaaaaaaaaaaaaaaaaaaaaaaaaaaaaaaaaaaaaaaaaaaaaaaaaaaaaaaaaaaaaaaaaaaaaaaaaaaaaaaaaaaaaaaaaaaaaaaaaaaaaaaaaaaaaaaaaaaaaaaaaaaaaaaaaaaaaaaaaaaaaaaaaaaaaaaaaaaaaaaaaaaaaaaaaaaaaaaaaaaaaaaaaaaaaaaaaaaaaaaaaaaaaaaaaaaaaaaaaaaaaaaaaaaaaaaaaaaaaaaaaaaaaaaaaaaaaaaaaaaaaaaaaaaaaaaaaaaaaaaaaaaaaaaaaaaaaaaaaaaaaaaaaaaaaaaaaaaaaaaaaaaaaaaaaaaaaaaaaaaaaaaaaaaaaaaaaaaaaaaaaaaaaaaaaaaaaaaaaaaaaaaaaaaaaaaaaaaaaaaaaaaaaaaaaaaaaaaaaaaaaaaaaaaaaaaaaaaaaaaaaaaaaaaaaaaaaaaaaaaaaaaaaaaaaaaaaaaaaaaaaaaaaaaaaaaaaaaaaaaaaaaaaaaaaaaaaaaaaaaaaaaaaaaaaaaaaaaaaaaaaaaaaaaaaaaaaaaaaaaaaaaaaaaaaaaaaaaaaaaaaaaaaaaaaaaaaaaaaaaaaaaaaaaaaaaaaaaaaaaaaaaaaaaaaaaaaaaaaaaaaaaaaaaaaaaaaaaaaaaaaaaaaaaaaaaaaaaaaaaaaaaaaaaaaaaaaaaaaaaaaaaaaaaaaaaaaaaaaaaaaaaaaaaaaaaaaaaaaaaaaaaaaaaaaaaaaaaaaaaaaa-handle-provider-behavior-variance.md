---
title: Handle provider behavior variance
description: 'LLM providers and models differ widely in timing, schema shape, and
  metadata reporting, so integration code must be written defensively against that
  variance rather than against the common case alone:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70968
---

LLM providers and models differ widely in timing, schema shape, and metadata reporting, so integration code must be written defensively against that variance rather than against the common case alone:

- **Timeouts**: Don't apply a single timeout value to both "time to first chunk" and "time between chunks" without checking how the underlying client resets those timers. Reasoning models can think for minutes without emitting any streamed text/reasoning delta, so a short `firstChunkMs` will abort valid requests. Prefer well-tested, generous defaults (e.g. the existing 5-minute timeout) over introducing a tighter one without verifying it against high-effort/reasoning model latency.
- **Schema/data normalization**: When normalizing provider-supplied JSON schemas (or other nested payloads), recurse into all nesting points — `items` (array/tuple forms), `anyOf`/`oneOf`/`allOf` branches, nested `properties` — not just the top level. A normalizer that only fixes the outer shape will silently miss deeply nested vendor quirks.
- **Capacity/metadata reporting**: When a vendor reports multiple conflicting capacity numbers (e.g. a model's configured max context vs. its currently loaded context), pick the safer (smaller) bound rather than the larger one, to avoid overflowing an actual constraint.
- **Vendor-specific special-casing**: Before adding bespoke handling for one provider (e.g. Bedrock's reasoning adapter), check whether the pattern already exists elsewhere, and consider whether the fix belongs upstream (in the provider's own SDK/adapter) instead of living as a local workaround. If a local workaround is unavoidable, keep it narrowly scoped and documented with why it exists.
- **Resolution correctness in tests**: When a test or comment claims a given code path is independent of catalog/registry lookups, verify that end-to-end — intermediate resolvers (e.g. model-ID rewriting against a generated catalog) can still take effect even when a model is explicitly registered. Name and scope tests/comments for what they actually exercise, not what was intended.

Example — normalizing nested schema types recursively instead of only at the top level:
```ts
function normalizeAiSdkToolInputSchema(schema: Record<string, unknown>): Record<string, unknown> {
  const normalized = { ...schema, type: typeof schema.type === "string" ? schema.type.toLowerCase() : schema.type };
  if (isRecord(normalized.items)) normalized.items = normalizeAiSdkToolInputSchema(normalized.items);
  for (const key of ["anyOf", "oneOf", "allOf"] as const) {
    if (Array.isArray(normalized[key])) {
      normalized[key] = (normalized[key] as unknown[]).map((branch) =>
        isRecord(branch) ? normalizeAiSdkToolInputSchema(branch) : branch,
      );
    }
  }
  return normalized;
}
```

Applying this standard means every provider/model integration should be validated against real streaming timing, deeply nested schema shapes, conflicting capacity metadata, and catalog-driven ID rewriting — not just the simplest documented case.</description>
