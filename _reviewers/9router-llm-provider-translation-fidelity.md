---
title: LLM provider translation fidelity
description: When writing adapters that translate between different LLM provider wire
  formats (OpenAI chat/completions, Responses API, Anthropic, Gemini, Zed, etc.) or
  route model IDs to providers, prioritize completeness and precision over broad assumptions.
repository: Decolua/9Router
label: AI
language: JavaScript
comments_count: 3
repository_stars: 31414
---

When writing adapters that translate between different LLM provider wire formats (OpenAI chat/completions, Responses API, Anthropic, Gemini, Zed, etc.) or route model IDs to providers, prioritize completeness and precision over broad assumptions.

1. Handle every content type the upstream can emit, not just plain text. Reasoning blocks, tool_calls/tool_use, and other structured content must be explicitly mapped through — silently dropping them breaks multi-turn agent workflows that depend on tool-call round-trips:
```js
// Bad: only handles text deltas, tool_use/tool_calls are dropped
function extractTextFromEvent(event) {
  const delta = event.choices?.[0]?.delta || {};
  return { text: delta.content || "" };
}

// Good: pass through tool calls/tool_use alongside text
function extractDeltaFromEvent(event) {
  const delta = event.choices?.[0]?.delta || {};
  return {
    text: delta.content || "",
    toolCalls: delta.tool_calls || delta.tool_use || null,
  };
}
```

2. Surface completion/truncation state accurately. When a response is incomplete (e.g. `max_output_tokens`, `content_filter`), report the correct `finish_reason` and don't emit partial/incomplete tool calls as if they were complete.

3. For model-to-provider routing, prefer narrow patterns tied to specific observed model IDs over broad version-based regexes. A loose rule like "all gpt-5.5+ go to provider X" can silently hijack future, unrelated model releases from their correct provider; scope the rule to the exact ID(s) that need it and let the catalog/explicit alias take precedence.

Add regression tests covering truncation states and tool-call pass-through for every new provider adapter.