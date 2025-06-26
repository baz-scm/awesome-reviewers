---
title: " Consistent test code style"
description: "Maintain consistent and clear testing patterns by following these guidelines: use strict equality assertions, prefer variable reassignment over block scoping for multiple sequential requests, and maintain consistent formatting to improve code readability and reduce unnecessary indentation."
repository: "fastify/fastify"
label: "Code Style"
language: "JavaScript"
comments_count: 6
repository_stars: 34000
---

Maintain consistent and clear testing patterns by following these guidelines:

1. Use strict equality assertions:
```javascript
// Incorrect
t.assert.equal(response.statusCode, 200)
t.same(JSON.parse(body), expectedValue)

// Correct
t.assert.strictEqual(response.statusCode, 200)
t.assert.deepStrictEqual(JSON.parse(body), expectedValue)
```

2. For multiple sequential requests, prefer variable reassignment over block scoping:
```javascript
// Avoid
{
  const response = await fastify.inject('/first')
  t.assert.strictEqual(response.statusCode, 200)
}
{
  const response = await fastify.inject('/second')
  t.assert.strictEqual(response.statusCode, 200)
}

// Prefer
let response = await fastify.inject('/first')
t.assert.strictEqual(response.statusCode, 200)

response = await fastify.inject('/second')
t.assert.strictEqual(response.statusCode, 200)
```

This approach improves code readability, reduces unnecessary indentation, and makes test flow easier to follow while maintaining variable scope control.