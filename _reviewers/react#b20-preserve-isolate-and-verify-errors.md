---
title: Preserve, isolate, and verify errors
description: 'When catching errors, never silently discard information about what
  actually failed. If you must suppress or convert an error, attach the original as
  `cause` (e.g. `new Error(''Failed to inspect hooks.'', {cause: error})`) or include
  it in any logged message, so the real failure is still debuggable. Be specific about
  which errors you are catching: check...'
repository: facebook/react#b20
label: Error Handling
language: JavaScript
comments_count: 9
repository_stars: 251895
---

When catching errors, never silently discard information about what actually failed. If you must suppress or convert an error, attach the original as `cause` (e.g. `new Error('Failed to inspect hooks.', {cause: error})`) or include it in any logged message, so the real failure is still debuggable. Be specific about which errors you are catching: check `error.code` or use `instanceof` to narrow (e.g. only swallow `ENOENT`, or check `RangeError` instead of matching on `message` text), and rethrow or surface anything unexpected rather than assuming the cause of a generic catch.

When a block invokes multiple independent operations — especially user-supplied callbacks, instruction handlers, or per-item work in a loop — wrap each operation in its own try/catch rather than one catch around the whole block, so a single failure doesn't prevent the rest from running. Pair any catch/response handling that owns a resource (e.g. a callback registered in a map) with `try/finally` to guarantee cleanup even if the handler itself throws, preventing leaks.

Finally, avoid error paths that silently produce a different (and wrong) result on failure — e.g. a fallback that swallows a read error and returns stale/undefined data. Prefer logging a warning or failing loudly (build failure, `console.error`) over quietly degrading behavior that could mask real problems.</description>
</invoke>
