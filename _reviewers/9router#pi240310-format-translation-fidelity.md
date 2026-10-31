---
title: Format-translation fidelity
description: 'When building adapters that translate requests/responses between API
  formats (e.g., Claude, OpenAI Chat Completions, OpenAI Responses), prioritize semantic
  correctness and safety over convenience:'
repository: decolua/9router#pi240310
label: API
language: JavaScript
comments_count: 4
repository_stars: 31756
---

When building adapters that translate requests/responses between API formats (e.g., Claude, OpenAI Chat Completions, OpenAI Responses), prioritize semantic correctness and safety over convenience:

1. **Avoid namespace collisions for injected/synthetic identifiers.** Any reserved tool name, id, or field the adapter injects (e.g., a fallback tool name) must first be checked against client-supplied names. If the client already uses that name, skip the injection/rewrite entirely rather than silently overwriting or shadowing client data — a collision can cause the proxy to execute the wrong tool.

```js
if (!toolNames.has(RESERVED_FALLBACK_NAME)) {
  preservedTools.unshift(buildFallbackTool(...));
}
// else: leave body untouched, do not inject
```

2. **Make structural rewrites idempotent and order-independent.** When rewriting a response's content/array based on matching items (e.g., tool_use blocks), track which items have already been processed (e.g., via an `insertedIds` set) instead of assuming a fixed ordering. Add tests for alternate orderings (e.g., client tool call before vs. after the intercepted call) to prevent duplicate or missing entries.

3. **Preserve response semantics faithfully across format boundaries.** Status/finish fields (e.g., `finish_reason`, `status`, `incomplete_details`) must reflect the true state of the upstream response — truncated or filtered output must not be reported as "completed"/`tool_calls` just because a tool call happened to be present. When mapping between formats, suppress partial/incomplete tool calls and report the correct truncation reason before considering any tool calls complete.

Every cross-format conversion function should have tests covering: collision scenarios for injected identifiers, multiple input orderings, and truncated/incomplete response states — not just the happy path.