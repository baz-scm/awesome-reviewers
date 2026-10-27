---
title: Callback Error Isolation
description: When executing user code (event handlers, scheduled callbacks, instruction
  processors) or critical error-trigger logic, ensure failures don’t break unrelated
  work and ensure the same behavior occurs in production.
repository: facebook/react#b5
label: Error Handling
language: JavaScript
comments_count: 7
repository_stars: 251886
---

When executing user code (event handlers, scheduled callbacks, instruction processors) or critical error-trigger logic, ensure failures don’t break unrelated work and ensure the same behavior occurs in production.

Apply this standard:
1) Wrap per-callback execution in try/catch
- Catch inside the loop so one callback’s failure doesn’t prevent later callbacks/phase flushing.
- If you register/track callbacks, use finally to prevent leaks.

Example (pattern):
```js
for (let i = 0; i < callbacks.length; i++) {
  try {
    callbacks[i](args);
  } catch (error) {
    // report/recover as appropriate for the system, but keep going
  }
}
```
2) Don’t make throwing behavior conditional on __DEV__
- Critical guards and throws must be active in production (e.g., move counters/tracking out of __DEV__).
- If something is only diagnosable in dev, prefer logging (console.error) over throwing.

3) Use stackless payloads for internal control-flow aborts
- For internal cleanup/abort signals, avoid capturing stacks (don’t use stackful Error); use strings/values with clear documentation, and ensure consumers already handle that shape.

4) Prevent later “success” signaling after fatal failures
- Once a fatal error occurs, ensure success paths (e.g., all-ready/completion notifications) cannot fire later due to pending/queued work. Prefer condition checks to ad-hoc mutation where possible.

These rules prevent “one failing callback breaks rendering”, missing production error detection, dev/prod divergence, and confusing/stack-dependent internal control flow.