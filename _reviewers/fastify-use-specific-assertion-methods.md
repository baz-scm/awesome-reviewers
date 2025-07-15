---
title: "Use specific assertion methods"
description: "Choose the appropriate assertion method based on the data type being tested. This improves test readability and provides clearer error messages when tests fail."
repository: "fastify/fastify"
label: "Testing"
language: "JavaScript"
comments_count: 15
repository_stars: 34000
---

Choose the appropriate assertion method based on the data type being tested. This improves test readability and provides clearer error messages when tests fail.

For scalar values (numbers, strings, booleans), use `strictEqual` instead of `equal` or `deepStrictEqual`:

```js
// ❌ Not ideal - less specific assertion
t.assert.equal(response.statusCode, 200)
t.assert.deepStrictEqual(fastify.hasRoute({ }), false)

// ✅ Better - correct assertion for scalar types
t.assert.strictEqual(response.statusCode, 200)
t.assert.strictEqual(fastify.hasRoute({ }), false)
```

For objects and arrays, use `deepStrictEqual` rather than `deepEqual` or `same`:

```js
// ❌ Not ideal - can miss type differences
t.assert.deepEqual(body.toString(), JSON.stringify({ hello: 'world' }))

// ✅ Better - ensures exact object equality
t.assert.deepStrictEqual(body.toString(), JSON.stringify({ hello: 'world' }))
```

When possible, combine assertions directly with awaited methods to reduce code verbosity:

```js
// ❌ Not ideal - unnecessary intermediate variable
const body = await response.text()
t.assert.deepStrictEqual(body, 'this was not found')

// ✅ Better - direct assertion
t.assert.deepStrictEqual(await response.text(), 'this was not found')
```

Ensure proper resource cleanup using `t.after()` hooks rather than closing resources at the end of tests:

```js
// ❌ Not ideal - may not run if test fails
fastify.close()

// ✅ Better - ensures cleanup even if test fails
t.after(() => fastify.close())
```