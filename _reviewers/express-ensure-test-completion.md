---
title: Ensure test completion
description: Tests must properly terminate by following appropriate asynchronous patterns.
  For asynchronous tests, always invoke the `done()` callback after assertions or
  use returned Promises. For synchronous tests, omit the `done` parameter entirely.
  Use Mocha's built-in assertion handling rather than manual try-catch blocks.
repository: expressjs/express
label: Testing
language: JavaScript
comments_count: 5
repository_stars: 67300
---

Tests must properly terminate by following appropriate asynchronous patterns. For asynchronous tests, always invoke the `done()` callback after assertions or use returned Promises. For synchronous tests, omit the `done` parameter entirely. Use Mocha's built-in assertion handling rather than manual try-catch blocks.

Poor pattern (test may hang on assertion failure):
```javascript
it('should verify response data', function(done) {
  request(app)
    .get('/notes')
    .expect(200, function(err, res) {
      if (res.body.length === 1 && res.body[0].title === "Text") {
        done(); // No 'else' path - test will hang if check fails
      }
    });
});
```

Better pattern:
```javascript
it('should verify response data', function(done) {
  request(app)
    .get('/notes')
    .expect(200, function(err, res) {
      if (err) return done(err);
      assert.strictEqual(res.body.length, 1);
      assert.strictEqual(res.body[0].title, "Text");
      done();
    });
});
```

Best pattern (using testing framework assertions):
```javascript
it('should verify response data', function(done) {
  request(app)
    .get('/notes')
    .expect(200)
    .expect(res => {
      assert.strictEqual(res.body.length, 1);
      assert.strictEqual(res.body[0].title, "Text");
    })
    .end(done);
});
```

For long-running tests, set appropriate timeouts to prevent false failures:
```javascript
it('should process many routes', function(done) {
  this.timeout(7500); // Extend timeout for complex operations
  // Test implementation
  // ...
  done();
});
```