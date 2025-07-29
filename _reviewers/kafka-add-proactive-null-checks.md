---
title: Add proactive null checks
description: Always add null checks before accessing methods or properties on objects
  that can potentially be null, especially when dealing with Java APIs or exceptional
  conditions like RejectedExecutionException.
repository: apache/kafka
label: Null Handling
language: Other
comments_count: 3
repository_stars: 30575
---

Always add null checks before accessing methods or properties on objects that can potentially be null, especially when dealing with Java APIs or exceptional conditions like RejectedExecutionException.

When working with Java collections that return null (unlike Scala collections that return Option), use appropriate null safety patterns:

```scala
// Before accessing methods on potentially null objects
if (task != null && !task.isDone) {
  // safe to call methods on task
}

// When working with Java Map.get() which can return null
val response = responses.get(partition)
assertNotNull(response)
result.fire(response)

// Alternative approach using Optional
val response = Optional.ofNullable(responses.get(partition))
assertTrue(response.isPresent)
result.fire(response.get)
```

This prevents NullPointerException at runtime and makes the code more robust, particularly when integrating Scala code with Java APIs or handling exceptional conditions where objects might not be properly initialized.