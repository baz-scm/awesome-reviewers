---
title: Always await promises
description: Consistently use the `await` keyword when working with Promise-returning
  functions to ensure proper execution flow and prevent race conditions. Missing awaits
  can lead to unexpected behavior where code continues execution without waiting for
  asynchronous operations to complete.
repository: oven-sh/bun
label: Concurrency
language: TypeScript
comments_count: 4
repository_stars: 79093
---

Consistently use the `await` keyword when working with Promise-returning functions to ensure proper execution flow and prevent race conditions. Missing awaits can lead to unexpected behavior where code continues execution without waiting for asynchronous operations to complete.

Common issues to watch for:
1. Built-in async functions like `Bun.sleep()` or `fetch()`
2. Custom async functions that return Promises
3. Promise-returning methods like `sink.end()` or `server.stop()`
4. Async operations within loops

```javascript
// Incorrect: Function continues executing immediately
async function processWithSleep() {
  Bun.sleep(1000); // Missing await!
  return new Response(html);
}

// Correct: Function properly pauses execution
async function processWithSleep() {
  await Bun.sleep(1000);
  return new Response(html);
}

// Incorrect: Could create race conditions
async function performOperation() {
  const res = await fetch(server.url);
  server.stop(); // Server might stop before response is processed
  expect(await res.text()).toContain("expected content");
}

// Correct: Ensures operations complete before cleanup
async function performOperation() {
  const res = await fetch(server.url);
  expect(await res.text()).toContain("expected content");
  await server.stop();
}
```

In loops with async operations, ensure each iteration properly awaits its results:

```javascript
// Incorrect: Results might not be processed in order
for await (const params of paramGetter) {
  callRouteGenerator(type, i, layouts, pageModule, params);
}

// Correct: Each iteration waits for completion
for await (const params of paramGetter) {
  await callRouteGenerator(type, i, layouts, pageModule, params);
}
```