---
title: Preserve chat message blocks
description: Treat `ChatMessage.blocks` (TextBlock, ThinkingBlock, ToolCallBlock,
  ImageBlock, CacheControl, etc.) as the single source of truth for message content,
  and be careful not to silently drop information when constructing, streaming, or
  converting messages. Several bugs stemmed from overwriting the full `blocks` list
  with only the new text, which erased...
repository: run-llama/llama_index
label: AI
language: Python
comments_count: 11
repository_stars: 52785
---

Treat `ChatMessage.blocks` (TextBlock, ThinkingBlock, ToolCallBlock, ImageBlock, CacheControl, etc.) as the single source of truth for message content, and be careful not to silently drop information when constructing, streaming, or converting messages. Several bugs stemmed from overwriting the full `blocks` list with only the new text, which erased previously-parsed tool calls or thinking content:

```python
# Bad: wipes out tool_calls/thinking that chat_from_gemini_response already produced
llama_resp.message.blocks = [TextBlock(text=content)]

# Better: update only the relevant block, or append accumulated text,
# keeping any ToolCallBlock/ThinkingBlock already present
for block in llama_resp.message.blocks:
    if isinstance(block, TextBlock):
        block.text = content
        break
```

Specific guidance:
- When streaming/accumulating responses, replace or update the specific block type being streamed (text, thinking) without discarding tool-call or other blocks already extracted.
- Prefer deriving tool calls from `ToolCallBlock` entries in `message.blocks` rather than duplicating them in `additional_kwargs["tool_calls"]`; if legacy `additional_kwargs` handling is kept for backward compatibility, make it a fallback, not a parallel source of truth, to avoid duplicate/conflicting tool calls.
- When merging or splitting content blocks (e.g., for chunking/token splitting), check whether block-specific metadata (like a `ThinkingBlock`'s provider signature) would be lost; if merge semantics aren't well understood for a block type, default to not merging/splitting it rather than risk corrupting provider-required data.
- When converting `ChatMessage` to a provider-specific payload, iterate over `message.blocks` and handle each block type explicitly (text, image via URL or base64, tool call, cache control) instead of assuming a single string `content`, so multimodal and tool-call information is not lost in translation.
- When copying or transforming a list of messages (e.g., for XML formatting or memory), copy the whole `ChatMessage`/block objects rather than just `content`, so multimodal and other block-specific data survives unchanged.

Following this reduces subtle regressions where tool calls, reasoning/thinking content, or multimodal data disappear during streaming, format conversion, or message transformation.