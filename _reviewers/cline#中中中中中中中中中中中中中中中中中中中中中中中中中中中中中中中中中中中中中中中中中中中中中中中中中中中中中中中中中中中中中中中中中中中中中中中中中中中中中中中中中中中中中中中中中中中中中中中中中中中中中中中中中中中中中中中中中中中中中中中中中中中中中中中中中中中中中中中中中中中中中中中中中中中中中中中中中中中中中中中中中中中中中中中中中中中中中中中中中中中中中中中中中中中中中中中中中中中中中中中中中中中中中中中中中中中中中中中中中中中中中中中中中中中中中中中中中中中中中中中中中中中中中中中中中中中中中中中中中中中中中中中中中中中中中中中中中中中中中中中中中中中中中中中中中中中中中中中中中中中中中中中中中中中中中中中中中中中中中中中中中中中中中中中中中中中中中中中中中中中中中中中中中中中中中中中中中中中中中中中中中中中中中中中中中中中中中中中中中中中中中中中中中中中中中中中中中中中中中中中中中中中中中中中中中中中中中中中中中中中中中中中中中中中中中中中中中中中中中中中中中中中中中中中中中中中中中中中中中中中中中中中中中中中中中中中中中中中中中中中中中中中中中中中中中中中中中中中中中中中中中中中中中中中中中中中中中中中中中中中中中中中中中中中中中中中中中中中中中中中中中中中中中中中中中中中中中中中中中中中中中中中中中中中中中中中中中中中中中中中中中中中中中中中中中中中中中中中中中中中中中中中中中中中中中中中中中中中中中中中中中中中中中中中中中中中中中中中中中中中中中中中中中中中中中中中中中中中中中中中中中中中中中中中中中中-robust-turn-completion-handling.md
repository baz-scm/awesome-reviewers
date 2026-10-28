---
title: Robust turn-completion handling
description: 'When interpreting or recovering from a model''s response, never rely
  on a single raw signal (finish reason, token count field, or message boundary) in
  isolation — inspect the actual content shape and scope it to the current turn. Specifically:'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70986
---

When interpreting or recovering from a model's response, never rely on a single raw signal (finish reason, token count field, or message boundary) in isolation — inspect the actual content shape and scope it to the current turn. Specifically:

- Scope any "facts about this run" extraction (edits made, errors seen, tools called) to messages belonging to the current turn/prompt, not the whole history, so injected context or prior turns don't leak into decisions like verify/review/fix.
- Treat a `stop` finish reason that produced only reasoning (no text, tool call, media, or provider-executed activity) as incomplete rather than a genuine answer, and route it through the same continuation path as an unknown/truncated finish.
- When recovering from truncated or degenerate turns (e.g. max-tokens, empty retries), never silently drop the partial answer or discard side effects that already happened — provider-executed tool activity recorded only in metadata must be preserved even if a later part of the same retry errors. If a retry itself comes back empty or aborted, keep the original truncated turn rather than replacing it with nothing.
- Normalize token usage defensively: providers report reasoning tokens in different shapes (top-level field, nested under `outputTokens.reasoning`, raw provider metadata, etc.) and always as a subset of output tokens, not additive. Strip reasoning tokens out of `outputTokens` consistently regardless of which shape a provider uses, and add a regression test for each new shape discovered so downstream consumers (session totals, telemetry, billing) don't double-count.

In short: build turn-outcome and usage-normalization logic test-first against the full matrix of finish-reason × content-shape combinations you can enumerate, and favor keeping a degraded-but-real result over losing it to a failed recovery or an incomplete classification.