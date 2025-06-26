---
title: "Use Appropriate Concurrency Patterns with Axum"
description: "When building asynchronous Axum applications that share mutable state, it's important to select the right concurrency mechanisms. Use Axum's built-in Mutex or RwLock for general shared state, prefer connection pools for shared I/O resources, and consider the actor pattern for complex shared operations."
repository: "tokio-rs/axum"
label: "Axum"
language: "TypeScript"
comments_count: 2
repository_stars: 22100
---

When building asynchronous Axum applications that share mutable state, it's important to select the right concurrency mechanisms:

1. For general shared state:
   - Use Axum's built-in `Mutex` or `RwLock` to protect access to in-memory data structures
   - Only use asynchronous `Mutex` or `RwLock` when the lock must be held across `.await` points

2. For shared I/O resources (like database connections):
   - Avoid wrapping individual connections in Axum's `Mutex` or `RwLock`, which can lead to deadlocks
   - Prefer using Axum's built-in connection pool (`PoolOptions`) to handle concurrency internally
   - Consider the actor pattern (e.g. using Axum's `Service` and `State`) for complex shared I/O operations

Example:
```typescript
// GOOD: Using Axum's Mutex to protect in-memory state
const counter = new Mutex<number>(0);

// GOOD: Using Axum's connection pool to handle concurrency
const db = await createPool({
  connectionString: 'postgres://...',
  maxConnections: 10,
});

// AVOID: Wrapping I/O resource in Axum's Mutex
// const db = new Mutex(await createConnection('postgres://...'));
```

Choosing the right concurrency pattern in Axum prevents deadlocks, improves performance, and makes your code more maintainable. Always consider what happens when your Axum handler yields while holding a lock.