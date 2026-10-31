---
title: Graceful async failure handling
description: When an operation depends on an external or async step, design the surrounding
  code so failures leave the system in a recoverable state rather than a broken one.
repository: cline/cline?foo=bar
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 71082
---

When an operation depends on an external or async step, design the surrounding code so failures leave the system in a recoverable state rather than a broken one.

1. Sequence state mutations after confirmed success. If an action (e.g., detaching a cloud session, switching UI state) is only valid once a dependent async step succeeds, perform the mutation after that step resolves — not before or in parallel. This way, a failure leaves the previous state intact and retryable instead of silently discarding something the user still needs.

```ts
// Bad: detaches before confirming the resume succeeded
detachCloudSession();
return await resumeSession(sessionId);

// Good: only detach once local resume is confirmed
const result = await resumeSession(sessionId);
detachCloudSession();
return result;
```

2. Prefer explicit state checks over parsing error messages. Don't infer failure causes by pattern-matching on error strings (e.g., detecting "no upstream" from a push error message). Instead, check the actual precondition directly (e.g., query `@{u}` for an upstream ref) so the logic is deterministic and doesn't break when error text changes.

3. For best-effort/fire-and-forget actions (opening a URL, non-critical background lookups) that shouldn't block or crash the UI, explicitly catch and swallow failures (`.catch(() => {})`) so they don't produce unhandled rejections, and tie any retry to the right trigger (e.g., retry on reconnect for a connection-dependent request, not on an unrelated event like account refresh).

Applying these practices ensures failures degrade gracefully, state stays consistent, and recovery/retry paths are predictable and testable.</description>
