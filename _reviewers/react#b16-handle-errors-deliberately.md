---
title: Handle Errors Deliberately
description: 'When adding/adjusting error paths, treat failure as part of the control
  flow: preserve the original abort/fatal reason, don’t silence errors, and isolate
  any potentially user/host code so one exception doesn’t break recovery/cleanup.'
repository: facebook/react#b16
label: Error Handling
language: JavaScript
comments_count: 10
repository_stars: 251891
---

When adding/adjusting error paths, treat failure as part of the control flow: preserve the original abort/fatal reason, don’t silence errors, and isolate any potentially user/host code so one exception doesn’t break recovery/cleanup.

Apply these rules:
1) **Don’t overwrite abort/fatal reasons or success callbacks**
- Guard “late” error/success handlers after a response is already closed/aborted/fatal.

2) **Isolate callback failures (especially user/host callbacks)**
- Wrap each callback invocation in its own try/catch so error handling doesn’t prevent flushing/cleanup that must still occur.

3) **Use consistent error signaling contracts**
- If you intentionally use a non-Error signal (e.g., internal cleanup string), ensure all consumer paths already support that shape.
- Avoid **conditional throws** that change behavior by environment; prefer logging or consistent error paths.

4) **Tests must assert errors, not silence them**
- If a code path can error/abort, tests should observe and assert the reason.

Example pattern (isolating callbacks while preserving recovery):
```js
function flushViewTransitionEvents(pendingEvents) {
  if (!pendingEvents) return;
  pendingEvents.forEach(event => {
    try {
      event();
    } catch (e) {
      // Convert/route to the appropriate error handling path, but
      // do not let this prevent subsequent required cleanup/flush.
      reportRecoverableError(e);
    }
  });
}
```

Checklist for PR authors:
- After an abort/fatal: what code prevents later “success” signaling or later errors replacing the reason?
- Are any callback invocations (user/host) wrapped so failures don’t break recovery/cleanup?
- Does the error value type (Error vs string) match what consumers already handle?
- Do tests assert the error/abort reason (no silent onError/do-nothing handlers)?