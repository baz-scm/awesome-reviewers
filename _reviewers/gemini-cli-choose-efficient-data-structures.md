---
title: Choose efficient data structures
description: Select data structures and algorithms that match your performance requirements
  rather than defaulting to simple but inefficient approaches. Consider the time complexity
  of operations and use specialized libraries when appropriate.
repository: google-gemini/gemini-cli
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 65062
---

Select data structures and algorithms that match your performance requirements rather than defaulting to simple but inefficient approaches. Consider the time complexity of operations and use specialized libraries when appropriate.

Key principles:
- Replace O(n) operations with O(1) alternatives when possible (e.g., use FixedDeque instead of array.splice() for queue operations)
- Use established libraries for complex algorithms (e.g., glob libraries instead of recursive directory traversal, minimatch for pattern matching)
- Choose data structures based on access patterns (e.g., deques for FIFO/LIFO operations, circular buffers for fixed-size collections)

Example from the discussions:
```typescript
// Avoid: O(n) splice operations on arrays
if (this.events.length >= this.max_events) {
  const eventsToRemove = this.events.length - this.max_events + 1;
  this.events.splice(0, eventsToRemove); // O(n) operation
}

// Prefer: O(1) operations with appropriate data structure
import { FixedDeque } from 'mnemonist';
// FixedDeque automatically handles overflow with O(1) operations
this.events = new FixedDeque(this.max_events);
this.events.push(newEvent); // O(1) with automatic FIFO overflow
```

Similarly, prefer `glob` libraries over recursive directory traversal, and `minimatch` over custom regex implementations for pattern matching. The performance benefits compound significantly as data sizes grow.