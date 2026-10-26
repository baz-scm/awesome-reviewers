---
title: Explicit Async Error Handling
description: 'Adopt a team-wide rule: error handling must be complete across async
  boundaries, correct in classification/retry eligibility, and explicit in user-visible
  outcomes.'
repository: cline/cline#v5
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 70864
---

Adopt a team-wide rule: error handling must be complete across async boundaries, correct in classification/retry eligibility, and explicit in user-visible outcomes.

**Standards**
1) **Never let errors escape “half-handled” async continuations**
- Prefer `await` with `try/catch`.
- If you use `.then(...)`, make sure exceptions thrown *inside* continuations are captured (i.e., turn them into rejections).

```ts
// ❌ Misses throws inside attach; can create unhandled rejections/hangs
void loadMxc().then((mxc) => spawn()).then(attach, onError);

// ✅ Captures both rejected promises and synchronous throws from attach
void loadMxc().then((mxc) => spawn()).then(attach).catch((err) => fail(err));
```

2) **Never create detached promises without an error sink**
- If you intentionally detach, always log/telemetry and/or ensure a safe UI/UX fallback.

```ts
// ❌ unhandled rejection possible
checkpoint.commit().then((hash) => update(hash));

// ✅ attach a catch
void checkpoint.commit()
  .then((hash) => update(hash))
  .catch((e) => logger.error("checkpoint commit failed", e));
```

3) **Retry only when the error type is known safe**
- Don’t widen whole-turn retry eligibility for timeouts or abort/cancel cases.
- Preserve correct attribution (timeout vs other failures) and ensure retries don’t repeat side effects.

4) **Fail clearly instead of silently changing behavior**
- When transferring/choosing between owners, sessions, or capabilities, avoid implicit fallbacks that can alter contracts.
- For torn/corrupt configuration reads, avoid silently disabling safety; either fail closed or surface a warning/telemetry.

5) **Make timer/telemetry lifecycles consistent with control flow**
- If the measured work never started (spawn/setup failed), cancel observation timers so you don’t emit false “ran for N seconds” samples.

**What this improves**: prevents unhandled rejections and hung states, ensures telemetry is trustworthy, and avoids incorrect retry behavior that can repeat actions or misrepresent the cause of failure.