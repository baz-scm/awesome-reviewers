---
title: Cross-format API translation
description: When building adapters that translate between different provider API
  shapes (streaming SSE events or full JSON bodies, e.g. OpenAI ⇄ Claude ⇄ Responses
  API), the translation state must be explicit and complete, never inferred from "last
  chunk wins" or implicit defaults.
repository: decolua/9router#testfrag
label: API
language: JavaScript
comments_count: 4
repository_stars: 31643
---

When building adapters that translate between different provider API shapes (streaming SSE events or full JSON bodies, e.g. OpenAI ⇄ Claude ⇄ Responses API), the translation state must be explicit and complete, never inferred from "last chunk wins" or implicit defaults.

Apply these rules:

1. **Guard terminal/duplicate events.** Track per-block and per-stream flags (e.g. `toolInfo.closed`, `state.finishReasonSent`, `state.messageStopSent`) so a late or repeated upstream chunk (like a trailing usage-only finish event) cannot re-emit already-closed blocks or a second `message_stop`. If such a chunk only carries new metadata (e.g. final usage), emit a minimal update (e.g. a usage-only `message_delta`) instead of replaying the whole sequence.

```js
if (!state.finishReasonSent) {
  state.finishReasonSent = true;
  state.finishReason = choice.finish_reason;
} else if (choice.usage && !state.messageStopSent) {
  results.push({ type: "message_delta", usage: choice.usage });
}
```

2. **Reconstruct, don't just grab the last chunk.** When collapsing a streamed sequence into a single non-streaming response, rebuild content from all relevant `content_block_*`/delta events and merge metadata (usage, stop reason) from the appropriate terminal event, rather than assuming the final chunk is complete.

3. **Make completion status explicit when mapping between response shapes.** When converting one API's result shape into another's (e.g. Responses `output[]` → Chat Completions `choices[]`), derive `finish_reason` from truncation/incomplete markers (`length`, `content_filter`, etc.) before considering tool calls complete, and suppress partial/incomplete data (e.g. unfinished tool-call arguments) so a truncated response is never misrepresented as a successful one.

4. **Declare capability/routing explicitly, not via fallback defaults.** When a model or endpoint doesn't declare supported formats/transports, don't let it silently inherit broad defaults (e.g. `null` meaning "unrestricted"); require explicit `supportedFormats`/transport declarations per model so routing to endpoints like `/responses` or `/messages` is intentional rather than an artifact of missing configuration.

Each of these cases should be covered by regression tests that exercise multi-chunk sequences, truncated/incomplete responses, and duplicate/late terminal events.</description>
</invoke>
