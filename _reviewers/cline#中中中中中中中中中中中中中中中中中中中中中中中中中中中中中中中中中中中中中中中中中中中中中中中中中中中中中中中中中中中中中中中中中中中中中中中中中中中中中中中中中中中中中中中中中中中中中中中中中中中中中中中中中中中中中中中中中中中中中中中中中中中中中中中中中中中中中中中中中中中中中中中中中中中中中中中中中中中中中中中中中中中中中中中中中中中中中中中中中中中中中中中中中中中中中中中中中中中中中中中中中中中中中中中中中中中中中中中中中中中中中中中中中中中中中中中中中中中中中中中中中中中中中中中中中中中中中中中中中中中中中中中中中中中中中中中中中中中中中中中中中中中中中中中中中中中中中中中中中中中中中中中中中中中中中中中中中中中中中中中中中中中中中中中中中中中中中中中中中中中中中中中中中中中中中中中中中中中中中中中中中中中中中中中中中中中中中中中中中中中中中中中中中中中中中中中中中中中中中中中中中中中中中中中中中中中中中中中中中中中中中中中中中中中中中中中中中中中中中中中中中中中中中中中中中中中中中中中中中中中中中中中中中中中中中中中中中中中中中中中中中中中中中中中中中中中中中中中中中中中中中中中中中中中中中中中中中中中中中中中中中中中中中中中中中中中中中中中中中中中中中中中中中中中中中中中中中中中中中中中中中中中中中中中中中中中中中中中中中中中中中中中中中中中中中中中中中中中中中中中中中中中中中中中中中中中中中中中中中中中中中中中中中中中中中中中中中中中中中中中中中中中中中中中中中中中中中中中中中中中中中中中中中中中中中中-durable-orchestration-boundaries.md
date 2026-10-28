---
title: Durable orchestration boundaries
description: Multi-step orchestrated sequences (e.g., push-then-create, or mutating
  live runtime state) must be driven from a durable, long-lived host rather than a
  client that can disconnect mid-sequence, and any state change applied to an in-flight
  execution must only commit at a verified, well-defined checkpoint boundary. Splitting
  a sequence of dependent steps...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Temporal
language: TypeScript
comments_count: 2
repository_stars: 70986
---

Multi-step orchestrated sequences (e.g., push-then-create, or mutating live runtime state) must be driven from a durable, long-lived host rather than a client that can disconnect mid-sequence, and any state change applied to an in-flight execution must only commit at a verified, well-defined checkpoint boundary. Splitting a sequence of dependent steps across a transient client leaves partial state on disconnect — e.g., a git branch gets pushed but the dependent task is never created, and a naive retry generates a new attempt id and pushes a duplicate branch instead of resuming. Move such sequences into the orchestrator/backend (e.g., a Hub or core service) so the whole sequence (prepare snapshot, push, create, initial send) executes as one unit that survives the client disconnecting, and is retry-safe because it is not dependent on viewer connectivity (though it still can't by itself survive a backend crash or host restart — that needs its own durability guarantee). Similarly, when mutating state on an active execution, distinguish between overrides that are safe to apply immediately to the current run and overrides that change behavior captured at run start (e.g., provider/model selection): only commit the latter at a verified suspended/checkpoint boundary, and defer them to the next fully rebuilt run otherwise, so in-flight work is never corrupted by a mutation applied at an arbitrary point. In short: own the full multi-step sequence in the durable component, and gate any state mutation behind an explicit, verified boundary rather than applying it opportunistically.</description>
</invoke>
