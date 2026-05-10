---
title: Preserve AI Structure Invariants
description: When working with LLM/chat “auxiliary” content (reasoning, tool calls/results,
  structured content blocks, and usage/metadata), enforce structural invariants so
  provider/streaming/truncation logic can’t silently corrupt meaning.
repository: langchain-ai/langchain
label: AI
language: Python
comments_count: 8
repository_stars: 136312
---

When working with LLM/chat “auxiliary” content (reasoning, tool calls/results, structured content blocks, and usage/metadata), enforce structural invariants so provider/streaming/truncation logic can’t silently corrupt meaning.

Practical rules:
- Normalize provider-specific formats into your internal canonical form (e.g., reasoning can arrive as strings vs list-of-dicts). Preserve edge semantics like empty strings.
- Treat `tool_calls` as the source of truth for tool-result validity; never emit/keep ToolMessages without a matching tool call, and avoid “reverse orphaning” when truncating/summarizing (keep the requesting AIMessage and its ToolMessages together atomically).
- In streaming, support the message-chunk aggregation contract (including `chunk_position="last"` semantics) so parsers can finalize partial JSON/tool arguments correctly.
- Don’t assume single vs batch shapes (`invoke` vs batched `generations`)—index into `LLMResult` consistently.
- Put extra metrics/fields into typed/appropriate containers (don’t add arbitrary keys to typed metadata objects); prefer `output_token_details` or `response_metadata` when extra keys aren’t supported.
- Add/adjust tests to validate invariants for both streaming and non-streaming paths (e.g., tool call chunk types, no orphaned/reverse-orphaned sequences).

Example (reasoning normalization + preserving empty semantics):
```python
from typing import Any

def normalize_reasoning(reasoning: Any) -> str | None:
    if reasoning is None:
        return None
    if isinstance(reasoning, str):
        return reasoning  # preserve ""
    if isinstance(reasoning, list):
        if not reasoning:  # empty list => None
            return None
        parts: list[str] = []
        for item in reasoning:
            if isinstance(item, dict):
                # support multiple provider shapes
                v = item.get("thinking") if "thinking" in item else item.get("content")
                parts.append("" if v == "" else str(v) if v is not None else str(item))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(reasoning)
```

Apply the same “invariant-first” mindset to tool-call/tool-result pairing and streaming chunk finalization: write code so the internal model never allows impossible states (or it is corrected immediately), and back it with targeted tests.