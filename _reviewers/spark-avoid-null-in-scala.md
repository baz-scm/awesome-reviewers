---
title: avoid null in Scala
description: Avoid using null values in Scala code and prefer Option types for representing
  optional values. Null usage can lead to NullPointerException at runtime and makes
  code less safe and predictable.
repository: apache/spark
label: Null Handling
language: Other
comments_count: 4
repository_stars: 41554
---

Avoid using null values in Scala code and prefer Option types for representing optional values. Null usage can lead to NullPointerException at runtime and makes code less safe and predictable.

When working with optional values, use Option[T] and handle the None case explicitly. For Java interoperability where null is required, use `.orNull` on the Option to convert safely:

```scala
// Avoid this
val aliasName = if (rightSideRequiredColumnNames.contains(name)) {
  generateJoinOutputAlias(name)
} else {
  null  // Dangerous - can cause NPE
}

// Prefer this
val aliasName = if (rightSideRequiredColumnNames.contains(name)) {
  Some(generateJoinOutputAlias(name))
} else {
  None
}

// When calling Java functions that expect null
javaFunction(aliasName.orNull)
```

This pattern is especially important when dealing with serializable classes where transient fields can become null after deserialization, potentially causing unexpected NPEs. Make fields private when they could be null due to serialization to prevent accidental access to null values.