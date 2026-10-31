---
title: API contract integrity
description: Treat request/response shapes, RPC method sets, and shared metadata as
  a single contract that every layer must honor consistently, not something each caller
  reinvents.
repository: cline/cline?foo=bar
label: API
language: TypeScript
comments_count: 6
repository_stars: 71082
---

Treat request/response shapes, RPC method sets, and shared metadata as a single contract that every layer must honor consistently, not something each caller reinvents.

- Round-trip every field: anything accepted on input must be forwarded through every corresponding output/event path. A field that goes in but never comes back out (e.g. a `displayPrompt` accepted by a session but dropped from the event that reports it) is a trap for the next integrator — add a regression test that pushes data through the full input→output cycle.
- Keep names truthful: if a header, field, or parameter's semantics change, rename it instead of silently repurposing it. Sending a `ulid` under a header still called `X-Task-ID` changes the contract without telling consumers.
- Single source of truth: derived/computed facts (e.g. "is this provider configured") belong in the one contract that owns them (a shared provider/catalog type); don't duplicate them into per-feature schemas that then have to be kept in sync by hand.
- Fully wire new operations: a new RPC/client method must be registered in every dispatch or allow-list that gates reachability (e.g. an operations registry), and a client should expose a method only if the underlying protocol actually supports it — remove or guard methods the backend can't fulfill rather than letting them fail at call time.
- Depend on abstractions, not one transport: a tool or client exposed from a shared package should be defined against an interface (e.g. a storage/session contract) that multiple backends (local, cloud) can satisfy, rather than being hard-wired to one implementation's requirements (auth tokens, session IDs, HTTP semantics).

Example of the naming trap to avoid:
```ts
// Before: header name no longer matches what it carries
"X-Task-ID": this.options.ulid || ""   // consumers still assume this is the task id

// After: name matches content, or both values are sent explicitly
"X-Task-ID": this.options.taskId || "",
"X-Task-ULID": this.options.ulid || "",
```