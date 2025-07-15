---
title: Optimize hot paths
description: 'When writing code that will be executed frequently (hot paths), prioritize
  performance optimizations that reduce overhead. This includes:


  1. **Move expensive operations out of frequently executed blocks**: Place resource-intensive
  operations like `require()` calls at module initialization rather than in request
  handlers or response methods.'
repository: expressjs/express
label: Performance Optimization
language: JavaScript
comments_count: 4
repository_stars: 67300
---

When writing code that will be executed frequently (hot paths), prioritize performance optimizations that reduce overhead. This includes:

1. **Move expensive operations out of frequently executed blocks**: Place resource-intensive operations like `require()` calls at module initialization rather than in request handlers or response methods.

```javascript
// Poor performance: Loading module on every response
res.send = function send(body) {
  // ...
  if (isChunkBlob) {
    var WritableStream = require('stream/web').WritableStream; // ❌ Executed on each call
    // ...
  }
};

// Improved: Load once at module initialization
const { WritableStream } = require('stream/web'); // ✅ Loaded once

res.send = function send(body) {
  // ...
  if (isChunkBlob) {
    // WritableStream is already available
    // ...
  }
};
```

2. **Use direct property assignments when values are trusted**: Avoid unnecessary method calls that add function invocation overhead.

```javascript
// Less efficient with method call overhead:
this.status(status); // ❌ Additional function call overhead

// More efficient direct assignment when appropriate:
this.statusCode = status; // ✅ Direct assignment is faster
```

3. **Prefer traditional loops over higher-order functions**: Use for loops instead of array methods with callbacks to avoid closure creation overhead.

```javascript
// Less efficient with closure overhead:
this.tracers.forEach(function(tracer) { // ❌ Creates closures
  tracer(app, req, res, event, date, args);
});

// More efficient:
for (let i = 0; i < this.tracers.length; i++) { // ✅ Avoids closure overhead
  this.tracers[i](app, req, res, event, date, args);
}
```

4. **Minimize object creation**: Avoid creating temporary objects in frequently executed paths, as object allocation and garbage collection are expensive.

```javascript
// Expensive - creating objects in a loop:
for (var i = 0; i < this.root.length; i++) {
  context = { root: this.root[i] }; // ❌ Creating objects each iteration
  match = this.lookup.call(context, path);
}

// Better - reuse objects or restructure code:
const context = {}; // ✅ Create once
for (var i = 0; i < this.root.length; i++) {
  context.root = this.root[i]; // Modify existing object
  match = this.lookup.call(context, path);
}
```

These optimizations are most impactful in code that executes frequently, such as middleware, request handlers, and utility functions used in tight loops. Always verify performance improvements with benchmarks when making changes to critical paths.