---
title: prefer simple APIs
description: Design APIs with simplicity in mind by avoiding unnecessary method overloads,
  reducing configuration options, and preferring single well-designed methods that
  handle all cases rather than multiple variants.
repository: apache/spark
label: API
language: Other
comments_count: 5
repository_stars: 41554
---

Design APIs with simplicity in mind by avoiding unnecessary method overloads, reducing configuration options, and preferring single well-designed methods that handle all cases rather than multiple variants.

When faced with API design choices, favor approaches that make the developer's life easier by providing a single, clear way to accomplish a task. Instead of creating multiple overloads or adding numerous configuration knobs, design one method that can handle all scenarios elegantly.

For example, instead of having two separate methods:
```scala
batchWrite.commit(messages)
batchWrite.commitWithOperationMetrics(messages, metrics)
```

Prefer a single method that always accepts the optional parameter:
```scala
// Always call commit with metrics parameter
// If no metrics, pass an empty Map
batchWrite.commit(messages, metrics.getOrElse(Map.empty))
```

This approach reduces the API surface area, eliminates the need for implementers to handle multiple code paths, and provides a consistent interface. Avoid creating "too many knobs" that complicate the API - instead, ask whether the functionality can be achieved through careful design of a single, flexible method.

The same principle applies to streaming APIs and data structures - prefer simple, direct approaches over complex batching or grouping mechanisms unless there's a clear performance or functional requirement that justifies the added complexity.