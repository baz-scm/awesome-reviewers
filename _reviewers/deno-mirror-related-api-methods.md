---
title: Mirror related API methods
description: When designing APIs with related method pairs (such as send/receive,
  input/output, or request/response), ensure their signatures and parameter structures
  mirror each other for consistency and developer ergonomics.
repository: denoland/deno
label: API
language: JavaScript
comments_count: 2
repository_stars: 103714
---

When designing APIs with related method pairs (such as send/receive, input/output, or request/response), ensure their signatures and parameter structures mirror each other for consistency and developer ergonomics.

Related API methods should have symmetric interfaces that make their relationship clear and predictable. This reduces cognitive load and prevents confusion about how data flows between paired operations.

Example of inconsistent API:
```js
// Inconsistent - send takes separate parameters, callback receives combined object
comm.send(data, buffers);
comm.onMessage(({data, buffers}) => { ... });
```

Example of consistent API:
```js
// Consistent - both use the same parameter structure
comm.send(data, buffers);
comm.onMessage((data, buffers) => { ... });
```

This principle applies to any paired operations where data structure or parameter patterns should logically correspond, ensuring developers can easily understand and predict the API behavior based on one method when using its counterpart.