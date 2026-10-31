---
title: Assert behavior, not wiring
description: A test must fail when the behavior it claims to cover regresses, and
  pass only because that behavior holds — not because it restates configuration, echoes
  a value the test itself just set, or grep's implementation source. Before merging
  a test, ask "would reverting the fix turn this red?" and "does my fake/stub enforce
  the same rules as the real...
repository: can1357/oh-my-pi
label: Testing
language: TypeScript
comments_count: 15
repository_stars: 37317
---

A test must fail when the behavior it claims to cover regresses, and pass only because that behavior holds — not because it restates configuration, echoes a value the test itself just set, or grep's implementation source. Before merging a test, ask "would reverting the fix turn this red?" and "does my fake/stub enforce the same rules as the real collaborator?".

Concretely:
- Don't assert static facts that mirror the DDL/config/field you just wrote (e.g. checking an index merely exists in `sqlite_master`, or that an options object lacks a key) when the real contract is an observable outcome (the planner uses the index, a keyless client still resolves the seeded catalog). Exercise the resolved/rendered result instead.
- Never read an implementation file's source text and assert on strings/comments found in it (`uiControllerSource.toContain(...)`). Drive the code path and assert its observable output; if the invariant needs to be enforced repo-wide, propose a lint rule, not a string scan over hundreds of call sites.
- When a hand-rolled test double (e.g. a fake `yieldQueue`, `ExtensionRunner`) is more permissive than the real collaborator (which gates on `register()`, requires a method that is optional-chained only in tests), the test can pass while the real path drops the behavior. Model the double after the real constraints, or exercise the real collaborator.
- Don't reach for banned type hacks (`as typeof x`, `Parameters<>`/`ReturnType<>`, `undefined as unknown as Model`) to force a branch or swap a method; use the sanctioned seam (`spyOn`/`mock.restore`, a supported setter/session configuration) so the test can't silently leak state or paper over a missing contract.
- For parameterized cases, make sure each row exercises a genuinely different branch — several inputs that fall through the same `undefined`/default path are redundant and should be collapsed.
- When rewriting or "strengthening" a test, verify no prior regression assertion was silently dropped (e.g. a terminal `session_stop` check, an empty-state wording pointer); keep or relocate it onto one of the remaining cases.

```ts
// Bad: restates config, no behavior exercised
expect(indexMap.has("idx_edges_type_source_target")).toBe(true);

// Good: exercises the consumer-visible outcome
const models = await resolveProviderModels(/* no api key */);
expect(models.map(m => m.id)).toEqual(["deepseek-v4-pro-0813"]); // seed survives, no roster fetch
```
