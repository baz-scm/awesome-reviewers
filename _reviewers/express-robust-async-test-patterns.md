---
title: Robust async test patterns
description: Write tests that exercise functionality the same way a real consumer
  would, and make sure asynchronous tests fail loudly rather than hanging. Prefer
  wiring behavior through the public API inside a request handler and asserting with
  supertest's `request(app).get('/').expect(...)`, instead of calling internal methods
  directly, testing an unrelated helper...
repository: Expressjs/Express
label: Testing
language: JavaScript
comments_count: 15
repository_stars: 69580
---

Write tests that exercise functionality the same way a real consumer would, and make sure asynchronous tests fail loudly rather than hanging. Prefer wiring behavior through the public API inside a request handler and asserting with supertest's `request(app).get('/').expect(...)`, instead of calling internal methods directly, testing an unrelated helper function, or constructing ad-hoc objects that don't match how the library is actually used:

```js
// Bad: tests an internal helper, not the actual behavior change
assert.throws(typeThrowError(name), TypeError)

// Good: exercises the change through the public API
it('should raise error for invalid status code', function (done) {
  var app = express()
  app.use(function (req, res) {
    res.sendStatus(1000)
  })
  request(app)
    .get('/')
    .expect(500, /Invalid status code/, done)
})
```

For async tests, always call `done()` on every path and guard assertions made inside callbacks with `try/finally` (or let them propagate) so a regression surfaces as a normal failure instead of a timeout:

```js
var server = app.listen(0, function () {
  try {
    assert.throws(function () {
      server.emit('error', new Error('boom'))
    })
  } finally {
    server.close(done)
  }
})
```

Avoid flakiness from hardcoded resources: use dynamic/ephemeral ports (`listen(0)`) instead of fixed port numbers that can collide across parallel runs, and size timeouts to tolerate slower CI/hardware rather than assuming a fast default. Keep new tests in the suite that matches the method under test (e.g. don't add `res.status` assertions inside `res.sendStatus` tests), and use the project's standard assertion library (`assert.strictEqual`, `assert.deepEqual`, `assert.throws`, or supertest's `.expect()`) instead of manual `if/else` checks or legacy libraries like `should` that mutate global prototypes.