---
title: Explicit API routing and translation
description: When building adapters that route requests or translate payloads between
  different provider/API formats (e.g. OpenAI, Claude, Responses), favor narrow, explicit
  declarations over broad defaults or regex-based fallbacks. A rule meant to fix one
  observed model/endpoint mismatch should match only that case, not a wide pattern
  (e.g. a version range) that could...
repository: decolua/9router
label: API
language: JavaScript
comments_count: 4
repository_stars: 31412
---

When building adapters that route requests or translate payloads between different provider/API formats (e.g. OpenAI, Claude, Responses), favor narrow, explicit declarations over broad defaults or regex-based fallbacks. A rule meant to fix one observed model/endpoint mismatch should match only that case, not a wide pattern (e.g. a version range) that could silently hijack future or unrelated IDs away from their correct transport. Document why each explicit mapping exists and what default path remains for everything else.

Equally, when translating between wire formats (streaming SSE events, non-streaming response bodies), make sure terminal/edge states are handled faithfully and idempotently:
- Don't re-emit terminal events (`content_block_stop`, `message_stop`) or duplicate state (tool call blocks) when multiple upstream "finish" signals arrive; guard with flags like `state.messageStopSent` and still forward late-arriving data (e.g. usage) via a minimal follow-up event.
- When output is incomplete/truncated, reflect that truthfully in the translated response (e.g. report `length`/`content_filter` as `finish_reason` and suppress partial tool-call fragments) rather than defaulting to a "success" finish reason.

Add regression tests for each specific routing/translation case (e.g. `tests/.../tool-arg-dedup.test.js`, truncation-with-partial-tool-calls tests) so future catalog or format changes don't reintroduce the bug.

Example guard pattern for idempotent terminal events:
```js
if (!state.finishReasonSent) {
  state.finishReasonSent = true;
  state.finishReason = choice.finish_reason;
}
```
