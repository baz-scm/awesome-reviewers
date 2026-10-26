---
title: API Contract Fidelity
description: 'When changing API-level behavior (RPC exposure, request headers, event
  envelopes, or capability/spec gating), preserve the contract end-to-end: semantics
  must match names, new fields must be forwarded through all layers, and published
  rules must be implemented exactly.'
repository: cline/cline#v22
label: API
language: TypeScript
comments_count: 4
repository_stars: 70886
---

When changing API-level behavior (RPC exposure, request headers, event envelopes, or capability/spec gating), preserve the contract end-to-end: semantics must match names, new fields must be forwarded through all layers, and published rules must be implemented exactly.

Apply this as a checklist:
- **Propagate new fields across the pipeline:** if a request/payload gains `X`, ensure every server projection / event copy / runtime handler includes `X` in the outgoing envelope; add a regression test that compares both payloads.
- **Do not change identifier meaning without renaming:** if `X-Task-ID` suddenly carries a different value (e.g., ulid), either keep the old meaning or rename (e.g., `X-Task-ULID`) / send both as separate headers.
- **Follow the spec unconditionally:** implement capability/visibility rules exactly as written; don’t add host-dependent exceptions that could leak disallowed items.
- **Keep RPC surfaces in sync:** ensure new operations are registered/exported so the client can reach them; if you rely on account-scoping, include/propagate a scope token so later operations can’t silently switch contexts.

Example (field propagation regression test pattern):
```ts
// Pseudocode: ensure `displayPrompt` is present in both copies
const serverEvent = projectPendingPromptSubmitted({ displayPrompt: "Hi" });
const runtimeEvent = hubRuntimeHostPendingPromptSubmitted(serverEvent);
expect(runtimeEvent.displayPrompt).toBe("Hi");
// also test omitted/empty string cases
```