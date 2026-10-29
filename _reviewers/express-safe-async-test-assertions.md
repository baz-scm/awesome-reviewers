---
title: Safe async test assertions
description: When asserting inside asynchronous callbacks (HTTP response handlers,
  `listen` callbacks, stream events, etc.), always guard assertions with `try`/`catch`
  (or `try`/`finally`) and guarantee that cleanup (`server.close()`) and the `done()`
  callback are invoked on both the success and failure path. An uncaught assertion
  thrown inside a callback is only caught...
repository: expressjs/Express
label: Testing
language: JavaScript
comments_count: 5
repository_stars: 69579
---

When asserting inside asynchronous callbacks (HTTP response handlers, `listen` callbacks, stream events, etc.), always guard assertions with `try`/`catch` (or `try`/`finally`) and guarantee that cleanup (`server.close()`) and the `done()` callback are invoked on both the success and failure path. An uncaught assertion thrown inside a callback is only caught by mocha's global exception handler, which prevents any following cleanup code from running and leaves the server/socket open, causing the suite to hang until a timeout instead of failing cleanly and quickly. Likewise, never swallow or ignore the `err` argument of callbacks such as `request(...).expect(200, function (err, res) { ... })` — check it (or return it) so real failures aren't silently lost, and make sure every async test path actually calls `done()`.

Example:

```js
var server = app.listen(0, function () {
  http.get('http://localhost:' + server.address().port, function (res) {
    var body = ''
    res.on('data', function (chunk) { body += chunk })
    res.on('end', function () {
      try {
        assert.strictEqual(res.statusCode, 404)
        assert.strictEqual(body, 'Not Found')
        server.close(done)
      } catch (err) {
        server.close(function () { done(err) })
      }
    })
  })
})
```

Apply this pattern consistently to any test performing assertions inside a callback, so failures are reported as normal test failures with proper cleanup rather than causing hangs or false positives.