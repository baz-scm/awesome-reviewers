---
title: LLM usage accounting
description: 'When integrating LLM provider APIs, treat capability and usage data
  defensively and favor the most conservative, actually-correct value rather than
  an optimistic or convenient one:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70970
---

When integrating LLM provider APIs, treat capability and usage data defensively and favor the most conservative, actually-correct value rather than an optimistic or convenient one:

- **Context window / limits**: prefer the value that reflects what the provider will actually serve, not just the advertised ceiling. e.g. LM Studio reports both `max_context_length` (model ceiling) and a loaded/`context_length` per instance (what's actually served, which can be much smaller); use the smaller/loaded value (or `min()` across reported fields) for `maxInputTokens`/compaction budgets so compaction triggers before the provider rejects the request, not after.
- **Usage/token metrics**: normalize provider-reported usage into one canonical shape before using it downstream. Reasoning tokens are often reported as a *subset* of `outputTokens` (e.g. OpenAI's `completion_tokens_details.reasoning_tokens`, or nested `outputTokens.reasoning` in some SDK versions) — strip them back out of `outputTokens` and track them separately so session totals, telemetry, and cost calculations don't double-book the same tokens. Add regression tests for each known provider shape rather than relying on a single hardcoded path.
- **Cost estimates for opaque payloads** (e.g. base64 images): use a flat, bounded per-item cost instead of scaling with encoded size, since real cost depends on semantic properties (e.g. pixel dimensions) that don't correlate with byte length.
- **Avoid vendor-specific branches when a shared capability model will do**: before adding bespoke per-provider logic (e.g. a Bedrock-only reasoning router), check whether the provider actually needs special casing or whether existing provider-agnostic capability data (e.g. "does this model advertise reasoning controls") already covers it. Push true adapter bugs upstream (e.g. to the AI SDK) rather than working around them locally when feasible.

Example — preferring the safe context value:
```ts
const contextWindow = Math.min(
  entry.max_context_length ?? Infinity,
  entry.loaded_context_length ?? Infinity,
);
```

Example — stripping reasoning tokens out of outputTokens:
```ts
// reasoning tokens are a subset of outputTokens, not additional to it
outputTokens: Math.max(0, normalizedUsage.outputTokens - reasoningTokenCount),
```

Applying this consistently prevents silent overflows (compaction firing too late), incorrect billing/telemetry (double-counted tokens), and unnecessary vendor-specific code paths that drift from upstream behavior.</description>
