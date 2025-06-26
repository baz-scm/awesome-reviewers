# Code Reviewers

Generated from: `../../../fastify_results_2.json`  
Total reviewers: **24**


## Reviewer 1: Write clear documentation

**Label:** `documentation`  
**Language:** `Markdown`  
**Discussion IDs:** 8 discussions  

### Description

Documentation should be clear, precise, and self-contained while following established style conventions. When writing technical documentation:

1. **Use precise language**: Clearly describe how APIs work, including any restrictions or requirements.
   ```js
   // Good
   // The function must be synchronous, and must not throw an error.
   fastify.setGenReqId(function (rawReq) { return 'request-id' })
   
   // Bad
   // This function can be used to set a request ID.
   fastify.setGenReqId(function (rawReq) { return 'request-id' })
   ```

2. **Make documentation self-contained**: Include all necessary context within the document itself rather than relying on external links.
   ```js
   // Good
   // The `preHandler` hook allows you to specify a function that is executed before
   // routes' handler.
   
   // Bad
   // See Issue #1234 for more details on the preHandler hook.
   ```

3. **Follow style conventions**: 
   - Avoid using "you" in reference documentation
   - Avoid contractions in formal documentation
   - Use proper formatting for headers, lists, and code blocks
   
   ```js
   // Good
   // When request logging is enabled, request logs can be customized by
   // supplying a createRequestLogMessage() function.
   
   // Bad
   // You can customize your request logs by using a createRequestLogMessage() function.
   ```

4. **Create accessible links**: Provide meaningful context in link text rather than using generic phrases.
   ```md
   <!-- Good -->
   [TypeScript no-floating-promises configuration](https://typescript-eslint.io/rules/no-floating-promises/)
   
   <!-- Bad -->
   Click [here](https://typescript-eslint.io/rules/no-floating-promises/) for more information.
   ```

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `b35089f8-dd9b-4605-b3e4-62f2c815bbff`
- `f4f9298c-4ea0-44d8-ba26-12210dbc2bd4`
- `8b64cd1d-5ab1-4906-9ab6-efa6d7521d82`
- `c6daad60-eff2-4365-bc4a-fdbd8bad8ea7`
- `00760325-c9af-4952-81a9-200183a00306`
- ... and 3 more

---

## Reviewer 2: Consistent test code style

**Label:** `code style`  
**Language:** `Javascript`  
**Discussion IDs:** 6 discussions  

### Description

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

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `41616a6d-d541-4a1f-bd67-8b18e647f943`
- `c344122c-48c7-4671-a971-e0123359d9c4`
- `c1faab39-492d-484c-84e2-a79cfd729558`
- `f4723faf-c657-4396-9b3b-e645e46ee55d`
- `76c29561-c6b3-4886-a950-255cb70b115b`
- ... and 1 more

---

## Reviewer 3: Concurrent operations completion management

**Label:** `concurrency`  
**Language:** `Javascript`  
**Discussion IDs:** 6 discussions  

### Description

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

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `41221cad-184d-46eb-a8fd-ae87827a8ef7`
- `9bd7a546-f1e2-4298-9629-771ef921cd0c`
- `1a49525c-ee53-4c98-acf0-eefcd8f1124c`
- `b4117342-dcef-43a8-b780-0b2640be9160`
- `775d9531-52bd-4442-8fd6-99fcbae99400`
- ... and 1 more

---

## Reviewer 4: Use specific assertion methods

**Label:** `testing`  
**Language:** `Javascript`  
**Discussion IDs:** 15 discussions  

### Description

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

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `e453b7bd-8396-4073-9da4-1d30117cf27d`
- `5633733e-944f-43d5-a550-654f71c77c95`
- `fb40f3ab-a87e-4752-a00f-72eb820db780`
- `75438886-7c68-4938-9bba-dbd48b870db7`
- `ebfc0276-d8b1-431d-88a6-bcd870cd5dce`
- ... and 10 more

---

## Reviewer 5: Consistent descriptive naming

**Label:** `naming conventions`  
**Language:** `Javascript`  
**Discussion IDs:** 4 discussions  

### Description

Use precise, consistent, and descriptive naming conventions throughout your code to enhance readability and maintainability. This includes:

1. Use past participle (adjective form) for variables storing processed data:
```javascript
// ✅ Good
const normalizedMethod = options.method?.toUpperCase() ?? ''

// ❌ Bad
const normalizeMethod = options.method?.toUpperCase() ?? ''
```

2. Choose function names that clearly describe their purpose without ambiguity:
```javascript
// ✅ Good
function addHTTPMethod(method, { acceptBody = true } = {}) {
  // Implementation
}

// ❌ Bad (confusing with HTTP Accept header)
function acceptHTTPMethod(method, { hasBody = false } = {}) {
  // Implementation
}
```

3. Use consistent naming patterns for related parameters and properties:
```javascript
// ✅ Good - consistent terminology
contentTypeSchemas[contentType] = compile({ schema: contentSchema, method, url, httpPart: 'body', contentType })

// ❌ Bad - inconsistent terminology
contentTypeSchemas[mediaName] = compile({ schema: contentSchema, method, url, httpPart: 'body' })
```

4. Name properties to clearly indicate their relationships:
```javascript
// ✅ Good - clear relationship between host and hostname
host: {
  get() { return this.raw.headers.host || this.raw.headers[':authority'] }
},
hostname: {
  get() { return this.host.split(':')[0] }
},
port: {
  get() { return this.host.split(':')[1] }
}
```

These conventions improve code understandability and reduce cognitive load for developers working in the codebase.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `14a295d4-0c13-4967-a1d3-e28a1041da55`
- `986bc368-cea1-43fa-8928-1049634f45f9`
- `cd8ad37a-f9f4-41c3-a59d-e1dd2e458868`
- `1fad1189-5775-4617-8d66-a2546647566a`

---

## Reviewer 6: Null safe patterns

**Label:** `null handling`  
**Language:** `Javascript`  
**Discussion IDs:** 5 discussions  

### Description

Use concise null checking patterns to prevent runtime errors and improve code readability when handling potentially undefined values. 

When checking if a value is neither null nor undefined:
```javascript
// Preferred: Concise null check
if (err != null) {
  // err is neither null nor undefined
}

// Instead of verbose explicit checks
if (err !== undefined && err !== null) {
  // Same result but more typing
}
```

Before accessing properties of objects that might be null/undefined:
```javascript
// Check before access to prevent "cannot read property of undefined" errors
if (reply.request.socket != null && !reply.request.socket.destroyed) {
  // Safe to use socket property
}
```

For default values, leverage nullish coalescing:
```javascript
// Assign default value if property is null or undefined
reply[kReplyHeaders]['content-type'] = reply[kReplyHeaders]['content-type'] ?? 'application/json; charset=utf-8'

// Or with fallback chains when appropriate
this[kRequestOriginalUrl] = this.raw.originalUrl || this.raw.url
```

These patterns ensure your code handles null and undefined values safely while remaining concise and readable.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `0e9294a8-edd4-4b56-be6f-4d8f82e7970a`
- `d6515102-b225-43f5-bc8b-f5de2a0d33e5`
- `fd6cd4d4-090a-420a-a412-47303f1db08f`
- `66ef58ba-a215-4a51-b1fa-e93c1964d059`
- `62c927bb-1f98-47ad-a041-ad48a9f9eefe`

---

## Reviewer 7: Preserve error context

**Label:** `error handling`  
**Language:** `Javascript`  
**Discussion IDs:** 5 discussions  

### Description

When handling errors, always ensure the original error context is preserved and properly surfaced. Error information should never be silently swallowed in try/catch blocks, as this makes debugging extremely difficult and can lead to unexpected system behavior.

There are two recommended approaches to preserving error context:

1. Use the standard `error.cause` property to maintain error chains:

```javascript
try {
  // Original operation
  const result = func(error, reply.request, reply);
  // Process result...
} catch (err) {
  // Preserve original error context
  if (!Object.prototype.hasOwnProperty.call(err, 'cause')) {
    err.cause = error; // Link the original error as the cause
  } else {
    // Log when unable to set cause to avoid losing context
    logger.warn({
      err: error,
      parentError: err,
      message: 'Original error cannot be linked as cause'
    });
  }
  
  // Propagate the error with context preserved
  throw err;
}
```

2. In asynchronous code, ensure proper promise rejection handling:

```javascript
// BAD: Double resolution if error occurs
sget(options, (err, response, body) => {
  if (err) reject(err)
  resolve({ response, body }) // Still runs after reject!
})

// GOOD: Return after rejection to prevent double resolution
sget(options, (err, response, body) => {
  if (err) {
    reject(err)
    return // Important! Prevents executing the resolve
  }
  resolve({ response, body })
})
```

Remember that proper error handling includes validation of your error conditions themselves. Be careful with falsy checks that might incorrectly handle empty strings or zero values as error conditions.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `9511a1e9-ac8b-427f-a3d3-5c2e4167dfb6`
- `9a1c2d0f-fad5-41fc-84bd-9487575359dd`
- `7ffa4928-786d-4001-8497-524e5a062560`
- `92e601c7-3726-4eaf-b932-7065df2d18b0`
- `ac00e7b8-e75e-42f5-aa88-d53624b0e86c`

---

## Reviewer 8: Support flexible logging

**Label:** `logging`  
**Language:** `Javascript`  
**Discussion IDs:** 2 discussions  

### Description

When designing logging interfaces, create flexible APIs that accommodate both standard and custom logging needs. This includes:

1. **Support custom log levels**: Don't assume only standard levels (trace, debug, info, warn, error, fatal) will be used. Always check against `logger.levels` which includes any custom levels.

2. **Allow message format customization**: Provide hooks that let users customize log message content.

3. **Enable level selection based on context**: Let users determine the appropriate log level dynamically based on runtime properties.

Example of a flexible logging interface:

```javascript
// Instead of this limited approach:
childLogger.info({ req: request }, 'incoming request')

// Provide a customization hook that gives control over both level and message:
function createRequestLogMessage(childLogger, req) {
  // User can choose log level based on request properties
  const level = req.headers['x-debug'] ? 'debug' : 'info'
  
  // User can customize the message content
  const message = `Incoming ${req.method} request to ${req.url}`
  
  // User controls both level and formatting
  childLogger[level]({ req: req, custom: true }, message)
}

// Usage
if (createRequestLogMessage) {
  createRequestLogMessage(childLogger, req)
} else {
  childLogger.info({ req: request }, 'incoming request')
}
```

This approach increases flexibility without sacrificing simplicity for common use cases.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `5df71b91-1a20-4107-a0d0-9656c542feb3`
- `9eae847d-dc44-4cad-b00f-db4bcb1509ab`

---

## Reviewer 9: Proper IPv6 address formatting

**Label:** `networking`  
**Language:** `Javascript`  
**Discussion IDs:** 2 discussions  

### Description

When constructing URLs with IP addresses, ensure IPv6 addresses are properly formatted according to RFC standards by wrapping them in square brackets. This applies to all IPv6 addresses, not just specific cases like localhost (::1). Additionally, use appropriate event handlers (`once` instead of `on`) for network events that should only be handled once per connection.

Code example for IPv6 address handling:
```javascript
// Incorrect - only handles a specific IPv6 address
const host = address.address === '::1' ? '[::1]' : address.address

// Correct - handles all IPv6 addresses according to RFC standards
const host = address.family === 'IPv6' ? `[${address.address}]` : address.address
```

Code example for proper event handling:
```javascript
// Incorrect - may cause multiple handlers to be registered
session.on('connect', function () {
  http2Sessions.add(session)
})

// Correct - ensures the handler is registered exactly once
session.once('connect', function () {
  http2Sessions.add(session)
})
```

Following these practices ensures compliance with RFC 3986 and RFC 2732 for URL formatting and prevents potential issues with network connection management.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `91e6ecbe-a238-4cd6-8f44-f7385b6d8d2e`
- `1508e3ef-41b7-47e5-b961-979bbf81db9b`

---

## Reviewer 10: Consistent JSDoc standards

**Label:** `documentation`  
**Language:** `Javascript`  
**Discussion IDs:** 5 discussions  

### Description

Document all public APIs and significant internal functions with comprehensive JSDoc comments that include accurate descriptions, parameter and return types, and any notable side effects. Follow standard JSDoc format conventions consistently across the codebase.

When documenting functions:

- Include clear descriptions of purpose and behavior:
```js
/**
 * Leverage light-my-request package to injects a fake HTTP request/response
 * into Fastify for simulating server logic, writing tests, or debugging.
 *
 * Warning: if the server is not yet "ready," this utility will force
 * the server into the ready state.
 *
 * @see {@link https://github.com/fastify/light-my-request}
 */
fastify.inject = setupInject(fastify, {
```

- Use proper JSDoc tag formats with types and descriptions:
```js
/**
 * @param {object} serverOptions the fastify server options
 * @returns {object} New logger instance, inheriting all parent bindings,
 * with child bindings added.
 */
```

- For utility functions, especially those used in tests, include explanation of parameters and execution flow:
```js
/**
 * Executes an array of asynchronous steps in sequence. Each step is a function
 * that takes a `next` callback as its argument. The `next` callback must be
 * called to proceed to the next step.
 *
 * @param {Function[]} steps - An array of functions representing the steps to execute.
 */
```

Maintain consistent formatting across all JSDoc comments. This improves code readability, makes API documentation generation more effective, and helps new developers understand the codebase more quickly.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `0a8814fa-74bd-4ac7-9040-714b3db1762b`
- `eb57da2c-645c-4b87-b4ad-b231c43fc489`
- `fd94bb8b-426d-4b45-aef6-80de43d67194`
- `a01b497a-96a9-4097-b3fb-91e15a63a0ce`
- `96e1d495-d2ba-4984-8c2b-07d7dcbb5a34`

---

## Reviewer 11: Content negotiation design

**Label:** `api`  
**Language:** `Javascript`  
**Discussion IDs:** 4 discussions  

### Description

When building APIs, implement proper content negotiation to handle various media types in both requests and responses. This ensures your API can work with different client requirements and maintain compatibility with diverse ecosystems.

Key practices include:

1. Explicitly define and check content types for requests
2. Implement content type-specific validation schemas
3. Handle different response formats appropriately (JSON, streams, buffers)
4. Support both native and polyfill implementations of web standards

For example, when defining route schemas with content-specific validation:

```js
fastify.post('/', {
  schema: {
    body: {
      content: {
        'application/json': {
          schema: jsonSchema
        },
        'application/octet-stream': {
          schema: binarySchema
        }
      }
    }
  }
})
```

When handling response objects, avoid tight coupling to specific implementations:

```js
// Instead of:
if (payload instanceof Response) {
  // handle response
}

// Prefer more flexible detection:
if (
  // node:stream
  typeof payload.pipe === 'function' ||
  // node:stream/web
  typeof payload.getReader === 'function' ||
  // Response (works with polyfills too)
  Object.prototype.toString.call(payload) === '[object Response]'
) {
  // handle response
}
```

This approach enables your API to work correctly with various clients and frameworks while maintaining a clean, standards-compliant design.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `4ac0e840-74ec-45ce-9701-9a7112a55562`
- `48aa48dd-c849-4c28-829b-d1f5d451d4b5`
- `c9551f30-e8f0-4b16-8349-8f6bd61a4a03`
- `cdf8cf7c-5984-4beb-a5c6-3551142b3be1`

---

## Reviewer 12: Benchmark before choosing methods

**Label:** `performance optimization`  
**Language:** `Javascript`  
**Discussion IDs:** 4 discussions  

### Description

Always benchmark different implementation approaches for performance-critical operations before selecting a method. Different approaches (like array operations, string parsing, or data iteration) can have significant performance implications that may not be intuitive.

Example comparing array operations:
```javascript
const Benchmark = require('benchmark')
const suite = new Benchmark.Suite()

suite
  .add('concat', function() {
    return ['cookie'].concat(['cookie2', 'cookie3'])
  })
  .add('push', function() {
    return Array.prototype.push.apply(['cookie'], ['cookie2', 'cookie3'])
  })
  .on('cycle', function(event) {
    console.log(String(event.target))
  })
  .on('complete', function() {
    console.log('Fastest is ' + this.filter('fastest').map('name'))
  })
  .run()
```

Key considerations:
- Use appropriate sample sizes and realistic test data
- Test in your target environment
- Consider memory implications alongside pure speed
- Document benchmark results to justify implementation choices

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `fa13e485-6e12-4893-9a55-65ed51cac3ee`
- `90efd67f-c447-46bb-9be3-be52462317f0`
- `072feb6f-55e8-4ae3-8ee0-e02fe42eae37`
- `ebd4576b-a0d7-42f9-ada5-4cbbee36a3c4`

---

## Reviewer 13: Secure Content-Type validation

**Label:** `security`  
**Language:** `Javascript`  
**Discussion IDs:** 1 discussions  

### Description

When implementing Content-Type validation, ensure regular expressions start with '^' or include ';?' to properly detect the essence MIME type. Improper validation patterns may create vulnerabilities to CORS attacks. 

For example, instead of using a pattern like:
```js
const contentTypeRegex = /json/;
```

Use one of these more secure approaches:
```js
const contentTypeRegex = /^application\/json/; // Anchoring with ^ ensures exact matches
// OR
const contentTypeRegex = /application\/json;?/; // Including ;? handles parameters properly
```

This ensures that malicious Content-Types like "faketype+json" cannot bypass your security validation mechanisms.

### Suggested Modules

- **** → `**/*.js`

### Discussion References

- `6ee84814-eab4-45b5-8f3b-e72536f67ad2`

---

## Reviewer 14: Type-safe API designs

**Label:** `api`  
**Language:** `Typescript`  
**Discussion IDs:** 5 discussions  

### Description

Design APIs with strong type safety to improve developer experience and catch errors at compile time. Avoid using `any` types when possible, carefully order generic parameters to support type inference, and ensure return types accurately reflect API behavior.

When designing APIs with generic parameters:
1. Consider how type inference will work for users of your API
2. Place automatically inferable parameters last in generic lists
3. Ensure return types accurately reflect response possibilities

For example, when defining route handlers that can return different response types:

```typescript
// Good: Strong typing for status codes and responses
server.get<{
  Reply: {
    200: string | { msg: string }
    400: number
    '5xx': { error: string }
  }
}>(
  '/',
  async (_, res) => {
    const option = 1 as 1 | 2 | 3 | 4
    switch (option) {
      case 1: return 'hello'               // typed as 200 response
      case 2: return { msg: 'hello' }      // typed as 200 response
      case 3: return 400                   // typed as 400 response
      case 4: return { error: 'error' }    // typed as 5xx response
    }
  }
)

// Bad: Using 'any' types or improper generic ordering that breaks type inference
function badExample<T = any>(req: any): any {
  // Types are lost, errors not caught until runtime
  return req.data;
}
```

When testing types, verify that constraints work as expected by explicitly checking the type constraints with test assertions.

### Suggested Modules

- **** → `**/*.ts`

### Discussion References

- `47cdd1b5-22a3-4875-8ea5-c1278f74abca`
- `3d209d60-1da0-401d-b820-9a61df978b28`
- `db4f5254-463d-4af6-be81-2eb4e605d7dc`
- `41ba705a-652d-4f03-bb06-dae4815652fd`
- `970a6f7c-7d93-442b-843f-d88d4e6fe8a0`

---

## Reviewer 15: Verify types in tests

**Label:** `testing`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions  

### Description

Use explicit type assertions in TypeScript tests to verify that types behave as expected across various scenarios. Include assertions for inheritance relationships, property types, and different response status codes. This helps catch type-related regressions early and ensures the type system correctly models your application's behavior.

Example:
```ts
instance.register(childInstance => {
  // Verify inherited properties maintain correct types
  expectType<void>(childInstance.testPropSync)
  expectType<string>(childInstance.testValueSync)
  expectType<number>(childInstance.testFnSync())
})

// Verify response types with different status codes
expectType<(payload?: string) => typeof res>(res.code(200).send)
// Add assertions for other status codes
```

### Suggested Modules

- **** → `**/*.ts`

### Discussion References

- `44080975-1a92-4c43-8727-d7d73e462f86`
- `8a14d473-598f-4312-863d-efccc67fc82f`

---

## Reviewer 16: Use bot identity

**Label:** `ci/cd`  
**Language:** `Yaml`  
**Discussion IDs:** 2 discussions  

### Description

When configuring Git operations in GitHub Actions workflows, especially for automated commits, use the GitHub Actions bot identity instead of personal user accounts. This clearly distinguishes automated actions from manual ones, provides better audit trails, and avoids personal attribution for system-generated changes.

**Implementation:**
```yaml
- name: Git Config
  run: |
    git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
    git config --global user.name "github-actions[bot]"
```

This approach ensures that commit history properly reflects which changes were made through automation versus direct developer intervention, making repository history more transparent and accurate. It also prevents confusion that might arise when commits appear to come from individuals but are actually from automated processes.

### Suggested Modules

- **** → `**/*.yml`
- **** → `**/*.yaml`

### Discussion References

- `9810f3ca-da3b-493b-b973-6eb3a602c318`
- `b4561bf7-f9bd-40f2-8f4d-0974f95b8aae`

---

## Reviewer 17: Adhere to Fastify Coding Conventions

**Label:** `fastify`  
**Language:** `Typescript`  
**Discussion IDs:** 5 discussions  

### Description

When implementing code that uses the Fastify package in Typescript, ensure the following conventions are followed:

1. **Avoid Contractions**: Use full words instead of contractions in code and comments. For example, use "it is" instead of "it's".

```typescript
// Incorrect
// app.get('/hello', (req, res) => res.send("it's working!"));

// Correct 
app.get('/hello', (req, res) => res.send("it is working!"));
```

2. **Use Oxford Commas**: Include an Oxford comma (serial comma) when listing three or more items in function parameters, middleware, or plugin configurations.

```typescript
// Incorrect
app.use(helmet, compression, morgan);

// Correct
app.use(helmet, compression, and morgan);
```

3. **Maintain Consistent Formatting**: Keep formatting consistent throughout the codebase, including:
   - Avoid emojis in function/variable names or comments unless used consistently
   - Use relative paths for internal Fastify plugin imports
   - Maintain consistent capitalization in function and variable names

Adhering to these conventions ensures the Fastify codebase remains readable, maintainable, and cohesive across different developers and components.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `f9a33879-6c5e-4e25-b3c7-e88637a36724`
- `4aeecec3-40e6-4ce4-b1c7-037d92a83d2b`
- `2b99e524-c1ac-4268-bd54-0cb14ebe4568`
- `c7f7a6a3-40fe-4c8c-bda3-7a40f96f0115`
- `284eedda-a5ab-4bbd-b054-c88ebfaaa264`

---

## Reviewer 18: Proper Handling of Promises in Fastify Implementations

**Label:** `fastify`  
**Language:** `Typescript`  
**Discussion IDs:** 4 discussions  

### Description

When implementing Fastify applications in TypeScript, it is important to follow consistent patterns for handling promises and respecting the framework's specific constraints. Avoid mixing async/await with callback styles, especially when registering routes, plugins, or parsers. Be aware that some Fastify methods are designed as thenables and do not require explicit awaiting.

For example, when registering content type parsers, do not use `await` as this can cause issues in Fastify:

```typescript
// INCORRECT: Mixing await with registration methods
await fastify.addContentTypeParser('application/json', async (req, body) => {
  // This causes issues in Fastify
});

// CORRECT: Don't use await when registering content type parsers
fastify.addContentTypeParser('application/json', async (req, body) => {
  // Proper usage without await
});
```

When decorating reply methods, ensure they return values for proper chaining:

```typescript
// INCORRECT: Missing return value
fastify.decorateReply('sendSuccess', function (data) {
  this.send({ success: true })
})

// CORRECT: Return this for chaining
fastify.decorateReply('sendSuccess', function (data) {
  return this.send({ success: true })
})
```

If using ESLint with `no-floating-promises`, configure exceptions for Fastify-specific promise patterns to avoid unnecessary warnings.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `4a754204-cc98-42bc-8934-c0e87a2986cf`
- `d718fbf5-03a5-4b82-b7f8-2815efb56702`
- `6120e263-6167-426e-a784-69de1968e2c6`
- `27157e3c-0095-43ed-aa9d-f81543e424ca`

---

## Reviewer 19: Ensure Proper Null Handling When Using Fastify Decorators

**Label:** `fastify`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions  

### Description

When working with Fastify decorators, always perform explicit null checks before accessing potentially undefined properties. Relying on implicit null handling can lead to subtle bugs and unexpected behavior. Instead, leverage Fastify's type-safe decorator APIs and type guards to ensure null safety at compile-time.

**Why?** Fastify decorators provide a powerful way to extend the functionality of your application, but they can also introduce the risk of accessing undefined values. Explicit null checks help make your code's intent clear and prevent cascading errors caused by missing dependencies.

**Example:**

```typescript
// ❌ Problematic - unclear if user decorator is missing
const user = request.user;
if (user && user.isAdmin) {
  // Execute admin tasks
}

// ✅ Better - use Fastify's type-safe decorator API
try {
  const user = request.getDecorator<User>('user');
  if (user.isAdmin) {
    // Execute admin tasks
  }
} catch (err) {
  // Handle missing decorator case explicitly
}

// ✅ Also good - use type guards to ensure null safety
request.raw.on('close', () => {
  if (isRequestDestroyed(request.raw)) {
    // Handle aborted request
  }
});

function isRequestDestroyed(raw: FastifyRawRequest): raw is FastifyRawRequest & { destroyed: true } {
  return raw.destroyed;
}
```

By following these practices, you can write more robust and maintainable Fastify applications that are less prone to null-related errors.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `1523a875-4d3b-49d1-9ce6-31534cbb3fd2`
- `d4b0675c-0cda-4318-b922-6ccbcc566abb`

---

## Reviewer 20: Properly Handle Errors in Fastify Applications

**Label:** `fastify`  
**Language:** `Typescript`  
**Discussion IDs:** 5 discussions  

### Description

When implementing error handling in Fastify applications, it is important to always throw instances of the Error class rather than primitive values or non-Error objects. This ensures that errors are properly propagated through the Fastify error handling chain.

If a Fastify plugin's error handler re-throws a non-Error value (such as a string or number), it will not propagate to parent context error handlers and instead will be caught by the default error handler. This can lead to unexpected behavior and make it difficult to debug issues.

For example, instead of:
```typescript
fastify.setErrorHandler((error, request, reply) => {
  // This will NOT propagate correctly to parent error handlers
  throw 'foo';
});
```

You should use:
```typescript
fastify.setErrorHandler((error, request, reply) => {
  // This will properly propagate through the error handling chain
  throw new Error('foo');
});
```

By consistently throwing Error instances, you can ensure that errors are properly handled and propagated throughout your Fastify application, leading to more robust and maintainable error handling.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `3e2fa222-2d05-4f4b-9350-0c8b7414ba60`
- `eb0a42ce-facb-40bf-bdd0-f678c29836a9`
- `c7f5a2db-6955-4c11-abdb-08bf79ce32cf`
- `617842c7-8074-4dbc-aca6-21b8bd234173`
- `ff0af29f-2bdb-49bf-b433-860f02c5148c`

---

## Reviewer 21: Explicit Configuration Usage in Fastify

**Label:** `fastify`  
**Language:** `Typescript`  
**Discussion IDs:** 5 discussions  

### Description

When using the Fastify framework in Typescript, ensure that all configuration options are explicitly declared and properly documented. This includes:

1. Clearly defining all required configuration parameters, including their data types and default values (with units where applicable).
2. Explicitly specifying any configuration constraints or mutually exclusive options.
3. Providing comprehensive examples that demonstrate the correct usage of Fastify configuration settings.

**Example - Poor Usage:**
```typescript
// Unclear timeout setting with no units
const fastify = Fastify({
  http2SessionTimeout: 72000 
});

// Incomplete schema definition
fastify.get('/route', {
  schema: {
    querystring: { name: { type: 'string' } }
  }
});
```

**Example - Recommended Usage:**
```typescript
// Clear timeout setting with units
const fastify = Fastify({
  http2SessionTimeout: 72000 // Timeout in milliseconds for HTTP/2 sessions
});

// Fully defined schema requirements
fastify.get('/route', {
  schema: {
    querystring: {
      type: 'object',
      properties: {
        name: { type: 'string' }
      },
      required: ['name']
    }
  }
});
```

By following these guidelines, you can ensure that your Fastify-based applications are properly configured and documented, reducing the risk of user confusion and configuration errors.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `641a5420-f2fb-44e7-b50c-723dedd2d588`
- `928c01f3-7ba8-4caa-9c80-0af10920d616`
- `1cf42147-210c-4c77-a05b-54b61beb861a`
- `2cdb6df6-a663-48b3-b5d7-07aee1e86f13`
- `2591237e-152d-467d-84d0-8333dcd46dd9`

---

## Reviewer 22: Consistent Fastify Package Naming and References

**Label:** `fastify`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions  

### Description

When implementing code using the Fastify package in Typescript, it is important to use consistent and accurate naming conventions for Fastify-related references:

- Always use the actual Fastify package name (`fastify`) rather than referring to the Fastify repository or other informal names.
- When referencing Fastify types, plugins, or other Fastify-specific concepts, use the correct Fastify terminology and casing (e.g. `FastifyInstance`, `fastify.get()`).
- Organize Fastify-related imports and references alphabetically to maintain consistency and make the code easier to navigate.

Example:
```typescript
// Preferred: Using the correct Fastify package name and terminology
import fastify, { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';

// Instead of informal references
import { createFastifyApp } from 'my-fastify-utils';

// Preferred: Alphabetized Fastify imports
import { FastifyPluginAsync } from 'fastify';
import fastifyAuth from '@fastify/auth';
import fastifyCors from '@fastify/cors';
```

Following these conventions will improve the maintainability of your Fastify-based codebase and make it easier for other developers to understand and work with the Fastify package correctly.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `d3ea4a88-0289-4ea4-8718-41e91fdaad1f`
- `fd1df066-fb35-4806-b4c0-9812dc8f751d`

---

## Reviewer 23: Secure Fastify Code Implementation

**Label:** `fastify`  
**Language:** `Typescript`  
**Discussion IDs:** 2 discussions  

### Description

This review focuses on secure implementation patterns when using the Fastify web framework in Typescript:

1. **Prevent Prototype Pollution Attacks**: Avoid direct property access on untrusted objects. Instead, use `Object.prototype` methods to safely access object properties:

```typescript
// Vulnerable approach
fastify.get('/route', (req, reply) => {
  console.log(req.params.hasOwnProperty('name')); // Potential prototype pollution vulnerability
  return { hello: req.params.name };
});

// Secure approach
fastify.get('/route', (req, reply) => {
  console.log(Object.prototype.hasOwnProperty.call(req.params, 'name')); // Safe property access
  return { hello: req.params.name };
}); 
```

2. **Protect Against Denial-of-Service Attacks**: Configure appropriate request timeouts, especially when deploying Fastify without a reverse proxy:

```typescript
const fastify = Fastify({
  requestTimeout: 120000 // Set a non-zero timeout (e.g., 120 seconds)
});
```

These security measures help mitigate common web application vulnerabilities when using the Fastify framework.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `2318eefd-16c6-4d42-a9db-7cb7abf34472`
- `3420c5b7-5c0c-412a-9eef-14f716a6f71f`

---

## Reviewer 24: Consistent Fastify Integration Patterns

**Label:** `fastify`  
**Language:** `Typescript`  
**Discussion IDs:** 3 discussions  

### Description

When implementing integrations and plugins using the Fastify framework, maintain consistent coding patterns and conventions:

1. Follow Fastify's recommended package naming conventions, using the `@fastify` scope for all Fastify-specific packages (e.g. `@fastify/kafka` instead of `fastify-kafka`).
2. Ensure integrations provide clear and comprehensive documentation of the specific protocol, system or service being integrated (e.g. "Plugin to interact with Apache Kafka message broker").
3. Use Fastify's built-in type definitions and decorators consistently across all plugins and integrations.
4. When referencing external protocol standards, include the full RFC reference with a period at the end of the description (e.g. "Plugin to add HTTP 103 Early Hints based on [RFC 8297](https://httpwg.org/specs/rfc8297.html).").

Example Fastify integration:

```typescript
import fastify, { FastifyInstance } from 'fastify';
import { FastifyKafka } from '@fastify/kafka';

const server: FastifyInstance = fastify();

server.register(FastifyKafka, {
  brokers: ['kafka1:9092', 'kafka2:9092'],
  topic: 'my-topic'
});

server.get('/messages', async (request, reply) => {
  const messages = await server.kafka.consume();
  return messages;
});
```

Consistent implementation of Fastify integrations and plugins improves maintainability, makes resources easier to discover, and ensures developers can quickly understand the purpose and usage of network-related features in Fastify applications.

### Suggested Modules

- **** → `**/*.md`

### Discussion References

- `6b138a0e-509c-4ceb-b17e-9bee50fbc29d`
- `7ff6be6f-89f6-4c11-baeb-7d60121564be`
- `207a4e25-f1eb-4288-a921-1472ff0be349`

---
