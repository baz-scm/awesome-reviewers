---
title: Meaningful null guards
description: Only add null/undefined checks where the value can legitimately be absent,
  and make the check reflect that reason. If the type system (or an earlier guard)
  already guarantees a value is non-null, don't add a silent defensive check "just
  in case" — if that assumption is ever wrong, it's a real bug and should surface
  as a crash/invariant rather than be...
repository: facebook/react#b19
label: Null Handling
language: JavaScript
comments_count: 11
repository_stars: 251893
---

Only add null/undefined checks where the value can legitimately be absent, and make the check reflect that reason. If the type system (or an earlier guard) already guarantees a value is non-null, don't add a silent defensive check "just in case" — if that assumption is ever wrong, it's a real bug and should surface as a crash/invariant rather than be swallowed. For example, prefer failing loudly:

```js
// Bad: silently hides a type violation
if (prevHook?.subHooks?.length > 0 && nextHook?.subHooks?.length > 0) { ... }

// Good: types guarantee non-null, so trust them and let a violation crash
if (prevHook.subHooks.length > 0 && nextHook.subHooks.length > 0) { ... }
```

Likewise, when an early-return/guard condition exists, any null check that follows should mirror that same condition exactly — if the guarded value is unexpectedly null anyway, that mismatch indicates a bug worth surfacing, not a case to quietly bail out of.

When a value can genuinely be `null` or `undefined` (e.g. optional config, platform APIs like `navigator`, or data read from JSON/across async boundaries), check broadly with `== null` or `?.`/`??` rather than `=== null`, since `undefined` is often just as valid an "absent" value and strict null checks can let `undefined` slip through:

```js
// Prefer: catches both null and undefined
if (div == null) { return; }

// Over: only catches null, misses undefined
if (div === null) { return; }
```

Be careful when refactoring manual null checks into optional chaining or nullish coalescing — double-check the resulting boolean logic, especially around negation, since `a && !a.startsWith(...)` and `!a?.startsWith(...)` are not equivalent and such refactors have introduced real logic bugs. Also keep `null` and `undefined` usage consistent as sentinel values throughout related code paths (don't compare against `null` in one place and set `undefined` in another), and always explicitly (re)assign nullable/optional state on every code path so stale values from a previous call can't leak into the next one.