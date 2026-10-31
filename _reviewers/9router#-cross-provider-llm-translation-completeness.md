---
title: Cross-provider LLM translation completeness
description: 'When writing executors/translators that convert between LLM provider
  formats (OpenAI, Claude/Anthropic, Gemini, Zed, etc.), make sure every provider-specific
  content type is handled completely and consistently, and that fix-up logic for upstream
  quirks is shared rather than duplicated:'
repository: decolua/9router#
label: AI
language: JavaScript
comments_count: 3
repository_stars: 31729
---

When writing executors/translators that convert between LLM provider formats (OpenAI, Claude/Anthropic, Gemini, Zed, etc.), make sure every provider-specific content type is handled completely and consistently, and that fix-up logic for upstream quirks is shared rather than duplicated:

- Tool calls: every response parser (streaming and non-streaming) must explicitly handle `tool_calls`/`tool_use` content blocks. Before shipping a new executor, check existing ones (e.g. cursor, kiro) for the pattern and verify tool-call deltas are passed through unchanged — silently dropping them breaks multi-turn agent workflows (Claude Code, Codex, Cline, etc.).
- Reasoning/thinking content: when stripping or mutating special fields like `reasoning_content` to control token bloat, account for other parts of the pipeline that depend on specific values (e.g. a short placeholder used for upstream validation). Use precise conditions (such as a length threshold) rather than unconditionally deleting the field, so you don't break downstream checks while still fixing the token-bloat issue.
- Request/response repair logic (e.g. fixing malformed/duplicated JSON in tool-call arguments from non-compliant models) should be implemented once in a shared module (e.g. `translator/concerns/toolArgs.js`) and imported by every translator that needs it, instead of being copy-pasted per provider. This keeps behavior consistent and avoids divergent bug fixes.

Example of centralizing shared repair logic instead of duplicating it per translator:
```js
// translator/concerns/toolArgs.js
export function repairDuplicatedJsonArguments(raw) { /* ... */ }
export function appendToolArgs(...) { /* ... */ }

// openai-to-claude.js and kiro-to-claude.js
import { repairDuplicatedJsonArguments, appendToolArgs } from "../concerns/toolArgs.js";
```

Treat any new provider adapter as needing parity with existing ones for tool-call handling and special content fields before merging.