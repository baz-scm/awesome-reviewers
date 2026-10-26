---
title: Provider-Aware AI Safeguards
description: When integrating with LLM SDKs/providers, make defaults and injected
  history semantics depend on the model/provider’s actual capabilities—and lock the
  edge cases down with tests.
repository: cline/cline#v4
label: AI
language: TypeScript
comments_count: 7
repository_stars: 70864
---

When integrating with LLM SDKs/providers, make defaults and injected history semantics depend on the model/provider’s actual capabilities—and lock the edge cases down with tests.

Apply these rules:
1) Don’t use “one size fits all” streaming/timeouts
- If a timer can cause valid requests to abort (e.g., reasoning models that don’t emit deltas early), only set `firstChunkMs` when the caller explicitly chose it, or default it to a value consistent with the request/streaming behavior.

```ts
// Only apply first-chunk timer when explicitly configured.
const firstChunkMs = timeoutMs === undefined ? undefined : timeoutMs;

const requestTimeout = {
  ...(firstChunkMs !== undefined ? { firstChunkMs } : {}),
  ...(timeoutMs !== undefined ? { chunkMs: timeoutMs } : {}),
};

await streamText({
  model,
  // ...
  timeout: requestTimeout,
});
```

2) Use provider manifests for default models
- Avoid hardcoded “last resort” model IDs in connectors. Prefer the provider’s `defaultModelId`, handle catalog-less/local placeholders correctly, and only fall back when necessary.

3) Keep prompts mode-correct and provider-consistent
- Build system prompts using the proper shared/provider prompt builder.
- Ensure required behaviors (e.g., commit/PR prompting) vary by agent mode (Plan vs act/yolo) according to user intent.

4) Only send supported model/reasoning fields
- Ensure request translation doesn’t accidentally include reasoning fields a provider rejects.
- Prefer fixes upstream in the AI SDK adapter rather than duplicating provider-specific special handling in your codebase.

5) Compute caps as safe floors/ceilings—not accidental reductions
- Treat synthesized defaults as floors unless the caller explicitly sets a cap.
- Preserve existing clamps (model/context) while allowing increases only when justified by the model’s advertised budget.

6) Preserve tool-call/tool-result pairing in message history
- When injecting additional context into a running chat, never insert user messages between an assistant `tool-call` and its corresponding `tool-result`.
- Add/adjust tests to assert the chosen behavior for resume/seeded edge cases—avoid silently dropping context.

If you follow the above, you reduce “works for some models, fails for others” issues and prevent subtle correctness bugs that only appear under streaming, tool usage, or resume paths.