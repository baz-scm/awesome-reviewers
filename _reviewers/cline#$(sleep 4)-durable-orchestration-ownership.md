---
title: Durable orchestration ownership
description: Multi-step workflows that produce external side effects (e.g., pushing
  a git branch, then creating a task; or updating schedules/tasks) must not have their
  orchestration state live only in an ephemeral client or sidecar process (e.g., in-memory
  WeakMaps). If the client disconnects or closes between steps, the workflow can be
  left half-done, and a naive...
repository: cline/cline#$(sleep 4)
label: Temporal
language: TypeScript
comments_count: 2
repository_stars: 70978
---

Multi-step workflows that produce external side effects (e.g., pushing a git branch, then creating a task; or updating schedules/tasks) must not have their orchestration state live only in an ephemeral client or sidecar process (e.g., in-memory WeakMaps). If the client disconnects or closes between steps, the workflow can be left half-done, and a naive retry can create duplicate side effects instead of resuming or rolling back safely. Move the orchestration into a durable, server-side component (the Hub/core) that owns the full sequence of steps so it can complete, retry idempotently, and survive viewer disconnects — even if it cannot guarantee recovery from a crash of that durable service itself.

Similarly, when deriving or folding state from a stream of events, don't assume incremental folding alone keeps state correct over time (e.g., stale "next run" times for schedules). Resync with the authoritative source after relevant change events, applying any events that arrive mid-resync as one additional fold step, and explicitly clear/expire derived fields that are missing from the authoritative response. This keeps durable state consistent instead of silently drifting.

Example pattern: instead of
```ts
await applyHandoffGit(plan); // push branch
await cloud.create(...);     // create task — may never run if app closes here
```
perform both steps inside the durable service's own transaction/handler, passing the inputs needed (e.g., `localGit`, `initialMessage`) so the server completes the push + creation + initial send without depending on the client remaining connected.