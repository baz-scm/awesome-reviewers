---
title: Propagate and clean up errors
description: Never swallow an error or silently end a response/stream — forward it
  to the correct error channel. In middleware/handlers that's `next(err)` so the configured
  error-handling pipeline (and not the handler itself) decides how to log/report it;
  for one-off operations with a user-supplied callback (e.g. `fn` in `sendFile`),
  send the error there instead of into...
repository: Expressjs/Express
label: Error Handling
language: JavaScript
comments_count: 13
repository_stars: 69580
---

Never swallow an error or silently end a response/stream — forward it to the correct error channel. In middleware/handlers that's `next(err)` so the configured error-handling pipeline (and not the handler itself) decides how to log/report it; for one-off operations with a user-supplied callback (e.g. `fn` in `sendFile`), send the error there instead of into `next`, and don't mix the two. Example from a stream write:

```js
try {
  chunk.stream().pipeTo(new WritableStream({
    write: function (c) { response.write(c, encoding); },
    close: function () { response.end(); }
  }));
} catch (err) {
  // don't just end() the response and hide the failure
  req.next(err);
}
```

When you attach one-off listeners (`'error'`, `'aborted'`, socket errors, etc.) to drive this forwarding, make sure to: 1) remove them once they've fired or once the operation completes, so they don't fire again and invoke `next`/callback a second time; 2) stop any in-flight pipe/stream when an error occurs, so it doesn't keep writing to an already-errored response; 3) add a `return` after handling the error/abort case instead of letting execution fall through to the success path. Prefer established, well-tested helpers (`on-finished`, `finished`, `querystring.unescape`, etc.) over hand-rolled socket/listener management, since they already handle these edge cases correctly and pass through the underlying error object. Finally, when raising errors for invalid input, always throw real `Error`/`TypeError` instances (never primitive strings) with clear, consistent, and factually correct messages that state what was expected and what was actually received.