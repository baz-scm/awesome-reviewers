---
title: Async error recovery
description: 'Treat every async operation as something that can fail, and design its
  failure path as carefully as its success path. Concretely: (1) Never let a fire-and-forget
  async call produce an unhandled rejection — wrap it with `.catch(() => {})` or an
  explicit handler, as with `void open(url, { wait: false }).catch(() => {})`, so
  a missing browser/handler degrades...'
repository: cline/cline#`sleep 4`
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70979
---

Treat every async operation as something that can fail, and design its failure path as carefully as its success path. Concretely: (1) Never let a fire-and-forget async call produce an unhandled rejection — wrap it with `.catch(() => {})` or an explicit handler, as with `void open(url, { wait: false }).catch(() => {})`, so a missing browser/handler degrades silently instead of crashing the UI. (2) Don't mutate shared or UI state optimistically before an async operation's outcome is known; perform the state transition only after success, and if it fails, roll the UI back to the actual confirmed state rather than to a stale "previous" value you captured before starting — e.g. detach a cloud session only after a local resume succeeds, and on a failed mode toggle resync the indicator to the runtime's true current mode, not to whatever was displayed before the attempt. (3) For failures that are likely transient (e.g. a request made during startup), avoid one-shot fetches with no recovery path — tie retries to a natural recovery signal such as reconnect, so the UI self-heals instead of requiring a reload. (4) When a clean failure signal is genuinely unavailable (e.g. platform API limitations), don't hack around it — document the limitation explicitly in code comments and ensure safe fallback behavior remains available (alternate UI affordances, menu actions, etc.) so users aren't blocked.