---
title: " Concurrent operations completion management"
description: "When running concurrent operations in tests, ensure all operations complete before concluding the test. Race conditions occur when your test calls done() or resolves before all async operations finish, leading to flaky tests or missed assertions."
repository: "fastify/fastify"
label: "Concurrency"
language: "JavaScript"
comments_count: 6
repository_stars: 34000
---

When running concurrent operations in tests, ensure all operations complete before concluding the test. Race conditions occur when your test calls `done()` or resolves before all async operations finish, leading to flaky tests or missed assertions.

**For multiple concurrent HTTP/API calls:**
```javascript
// AVOID: Race condition - test might complete before all operations finish
test('API calls', (t, testDone) => {
  sget(url1, (err, res) => {
    t.assert.ifError(err)
    t.assert.strictEqual(res.statusCode, 200)
    testDone() // BAD: Other calls might still be running!
  })
  sget(url2, (err, res) => { /* assertions */ })
})

// BETTER: Use Promise.all for truly concurrent operations
test('API calls', async (t) => {
  const results = await Promise.all([
    fetch(url1),
    fetch(url2),
    fetch(url3)
  ])
  
  // All operations are complete before assertions run
  t.assert.strictEqual(results[0].status, 200)
  t.assert.strictEqual(results[1].status, 200)
})

// ALTERNATIVE: Use completion counter for callback style
test('API calls', (t, testDone) => {
  let pending = 3
  function completed() {
    if (--pending === 0) {
      testDone()
    }
  }
  
  sget(url1, (err, res) => {
    t.assert.ifError(err)
    t.assert.strictEqual(res.statusCode, 200)
    completed()
  })
  sget(url2, (err, res) => {
    t.assert.ifError(err)
    completed()
  })
  sget(url3, (err, res) => {
    t.assert.ifError(err)
    completed()
  })
})

// UTILITY APPROACH: Use waitForCb or similar utilities
test('API calls', (t, testDone) => {
  const completion = waitForCb({ steps: 3 })
  
  sget(url1, (err, res) => {
    t.assert.ifError(err)
    t.assert.strictEqual(res.statusCode, 200)
    completion.stepIn()
  })
  sget(url2, (err, res) => {
    // assertions
    completion.stepIn()
  })
  sget(url3, (err, res) => {
    // assertions
    completion.stepIn()
  })
  
  completion.patience.then(testDone)
})
```