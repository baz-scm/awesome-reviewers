---
title: Durable, scoped orchestration state
description: Multi-step workflows that must survive disconnects, crashes, or restarts
  should own their state and continuation logic in a durable, server-side component,
  not in ephemeral client/process memory (e.g., WeakMaps in a sidecar process). If
  a client disappears mid-sequence (e.g., after a git push but before task creation),
  the durable owner must be able to...
repository: cline/cline?ref=main
label: Temporal
language: TypeScript
comments_count: 3
repository_stars: 70980
---

Multi-step workflows that must survive disconnects, crashes, or restarts should own their state and continuation logic in a durable, server-side component, not in ephemeral client/process memory (e.g., WeakMaps in a sidecar process). If a client disappears mid-sequence (e.g., after a git push but before task creation), the durable owner must be able to resume or safely retry without duplicating side effects; design each step to be idempotent or resumable from the last known durable state rather than restarting blindly.

When tracking deadlines, timeouts, or recovery windows for async operations, scope them to the specific unit of work (e.g., a single acknowledged run/command), not to a broader resource like a socket connection. Only clear a deadline when you receive definitive, correlated evidence of completion for that exact operation — a matching reply, terminal event, or heartbeat — never on incidental events (like reconnection) that don't prove the operation finished. This prevents both premature deadline clearing (masking real hangs) and indefinite hangs when expected signals are missed.

For state rebuilt from event logs/folds, ensure your reducer correctly resubscribes to all relevant change events and explicitly reconciles entries that disappear from bounded replies (e.g., clear `nextRunAt` for schedules missing from a limited result set) rather than leaving stale state. Cover both replay-from-log and live-update paths with tests.

Example pattern for scoped deadlines:
```ts
// Bad: deadline cleared on any successful reconnection
this.reconnectAttempt = 0;
if (this.recoveryDeadline) clearTimeout(this.recoveryDeadline);
this.recoveryDeadline = undefined;

// Good: deadline is per-run, cleared only by that run's own completion signal
runDeadlines.get(runId)?.clearOnCorrelatedReplyOrTerminalEvent();
```
Applying this consistently avoids orphaned state after client disconnects, duplicate work on retries, hung commands when events are dropped, and stale derived state in event-sourced folds.