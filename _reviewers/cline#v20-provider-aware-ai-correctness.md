---
title: Provider-Aware AI Correctness
description: When implementing AI/LLM features, treat correctness as a combination
  of (1) strict execution boundaries (turn/state/tool pairing/prompt injection) and
  (2) provider-accurate budgeting and API-shape mapping. Bake these assumptions into
  code structure and tests.
repository: cline/cline#v20
label: AI
language: TypeScript
comments_count: 9
repository_stars: 70886
---

When implementing AI/LLM features, treat correctness as a combination of (1) strict execution boundaries (turn/state/tool pairing/prompt injection) and (2) provider-accurate budgeting and API-shape mapping. Bake these assumptions into code structure and tests.

Practical rules:
1) Scope computations to the current “real” turn
- Don’t let earlier-turn edits/errors influence verification/correction logic.
- Implement turn scoping based on the latest genuine user prompt (not reminders/steering/context).

2) Preserve tool-call adjacency invariants
- Never inject messages that break provider expectations for tool-call/tool-result pairing.
- If you buffer context, ensure it is emitted in the correct position or explicitly reject/handle unsupported resume shapes.

3) Use the right provider/model metadata fields
- Catalog fields are provider-specific; don’t rely on one generic name.
- Prefer “loaded”/effective limits over “max” ceilings when available (e.g., LM Studio’s `loaded_context_length`).
- Add support for provider-specific window fields (e.g., vLLM `max_model_len`).

4) Make token/budget math explicit and testable
- For non-text blocks (images), use a flat cost model and an image-aware serializer so cost doesn’t scale with base64 size.
- Clearly distinguish floors vs ceilings in max-output logic.
- Any “theoretical under-count” should be bounded and justified, not left unaddressed.

5) Pin provider adapter behavior with targeted tests
- Ensure invalid or unsupported fields (e.g., Bedrock reasoning fields for models without reasoning support) are never sent.
- If you find a recurring provider-adapter issue, prefer upstreaming to the adapter over spreading special handling across your codebase.

Illustrative patterns:
- Turn-scoped facts:
```ts
// Only consider messages after the newest real user prompt.
// (Conceptually: ignore steering/reminders with userRunSpan: 0.)
export function factsOf(messages: readonly AgentMessage[], result: AgentRunResult) {
  const edits = new Map<string, string | undefined>();
  let toolErrored = false;
  // ...iterate tool-call/tool-result parts only within the scoped range...
  return { status: 'completed', filesEdited: edits.size, toolErrored };
}
```
- Tool-pair adjacency guard:
```ts
private async flushPendingHookContexts() {
  if (!this.pendingHookContexts.length) return;
  const last = this.state.messages.at(-1);
  if (last?.role === 'assistant' && last.content.some(p => p.type === 'tool-call')) {
    // Keep context buffered to avoid breaking tool-call/tool-result pairing.
    return;
  }
  // ...inject buffered context as a single user message... 
}
```
