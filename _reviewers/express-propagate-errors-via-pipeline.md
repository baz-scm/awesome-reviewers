---
title: Propagate errors via pipeline
description: 'Never swallow, locally render, or silently drop an error — always let
  it flow through the standard error-handling mechanism so it can be centrally logged,
  customized, and surfaced consistently. Concretely:'
repository: expressjs/Express
label: Error Handling
language: JavaScript
comments_count: 8
repository_stars: 69579
---

Never swallow, locally render, or silently drop an error — always let it flow through the standard error-handling mechanism so it can be centrally logged, customized, and surfaced consistently. Concretely:

- Prefer passing errors to `next(err)` (or the equivalent callback-style `(err, result)`) instead of wrapping every handler in `try/catch` and responding inline. Frameworks like Express already catch synchronous throws and route them to error-handling middleware/finalhandler, so manual catch blocks that just format and send a response bypass customization (log formatting, custom error pages, status differentiation) that the central handler provides.

```js
// Avoid: swallowing/forwarding the error yourself with a generic response
app.get('/note/:id', function (req, res) {
  try {
    var note = noteUseCase.getById(req.params.id);
    res.json(note);
  } catch (err) {
    res.status(404).json(err.message); // loses stack/logging, forces same status for all errors
  }
});

// Prefer: let the error flow to centralized error-handling middleware
app.get('/note/:id', function (req, res, next) {
  noteUseCase.getById(req.params.id, function (err, note) {
    if (err) return next(err); // centralized logging/status mapping happens here
    res.json(note);
  });
});
```

- When wiring up event-based error sources (sockets, streams, child emitters), make sure the error listener is actually attached/removed at the right time: remove one-off listeners once the operation succeeds so later errors use normal `EventEmitter` semantics, and always clean up listeners when the operation completes to avoid leaks or stale handlers consuming real errors.
- Route errors to the correct destination only: e.g. an aborted request's error should go to the request-specific callback (`fn`) if provided, never leak into the general `next` error pipeline, and vice-versa.
- When refactoring a synchronous lookup/computation into an async operation, adopt the idiomatic `(err, result)` callback signature instead of returning a bare value, so downstream failures (e.g., a DB lookup) can be reported instead of silently returning `undefined`.
- Double-check that error paths actually execute: a commonly missed bug is constructing an `Error`/`TypeError` object without the `throw` keyword, which leaves the invalid state unreported. Always write and test the failure path explicitly.
- Any user-visible runtime behavior change around error propagation (e.g., no longer swallowing an error that used to be silently dropped) should be called out in the changelog, since it can surprise consumers who relied on the old behavior.

Following this standard keeps error handling predictable, centralizes logging/formatting concerns, and avoids both silent failures and duplicated inline error-response logic across handlers.