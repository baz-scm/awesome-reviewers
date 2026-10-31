---
title: Match nullability to guarantees
description: 'Null/undefined checks, optional chaining, and non-null assertions must
  reflect the actual type contract and runtime invariants — not an assumed one.


  - Don''t add defensive `?.`, `??`, or `!== undefined` checks for values the type
  system already guarantees are present. If `AssistantMessage.provider` is typed as
  required, `message.provider !== undefined` is...'
repository: can1357/oh-my-pi
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 37317
---

Null/undefined checks, optional chaining, and non-null assertions must reflect the actual type contract and runtime invariants — not an assumed one.

- Don't add defensive `?.`, `??`, or `!== undefined` checks for values the type system already guarantees are present. If `AssistantMessage.provider` is typed as required, `message.provider !== undefined` is dead code that obscures intent; if `SegmentContext.options` is non-optional, use `ctx.options.usage ?? {}` instead of `ctx.options?.usage ?? {}`. When a fixture or test forces an invalid shape via `as unknown as T`, fix the fixture instead of weakening production code.
- Don't use a non-null assertion (`this.#persist!.foo`) unless the invariant truly holds on every call path. If some callers can reach the code without the field being set (e.g., a memory-only instance with no `persist`), guard explicitly or set a flag that already accounts for that state, rather than asserting and crashing with `TypeError: undefined is not an object`.
- When collapsing an optional value with `??` into a shared key, cache slot, or default, verify the fallback can't be confused with a real value from a different context. `sessionId ?? ""` makes every session-less caller share one cooldown key; scope the fallback (e.g., per-instance state) so distinct "absent" cases don't collide.
- Prefer existing centralized parsing/normalizing helpers (e.g., `parseServiceTier()`) over re-implementing null/undefined/empty-string handling by hand — they already encode the correct absent-vs-falsy semantics and stay in sync when the underlying union changes.

Example:
```ts
// Bad: type already guarantees `provider` is defined — this check is dead and misleading
const failingModel = message.provider !== undefined && registry.find(message.provider);

// Good: trust the type, let `find()` signal "not resolvable" via its own return value
const failingModel = registry.find(message.provider);

// Bad: asserts an invariant that doesn't hold on every call path
async #ensureLoaded(): Promise<void> {
  this.#indexLoadPromise ??= this.#loadIndex(this.#persist!.indexPath);
}

// Good: guard for the case where the invariant doesn't apply
async #ensureLoaded(): Promise<void> {
  if (!this.#persist) return;
  this.#indexLoadPromise ??= this.#loadIndex(this.#persist.indexPath);
}
```