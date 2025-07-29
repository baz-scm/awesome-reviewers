---
title: catch specific exceptions
description: Avoid catching overly broad exception types like `Throwable` or `Exception`
  when you can be more specific about the expected failure modes. Catching `Throwable`
  is particularly dangerous as it captures JVM-level errors like `OutOfMemoryError`
  that should typically cause the application to exit.
repository: apache/kafka
label: Error Handling
language: Java
comments_count: 4
repository_stars: 30575
---

Avoid catching overly broad exception types like `Throwable` or `Exception` when you can be more specific about the expected failure modes. Catching `Throwable` is particularly dangerous as it captures JVM-level errors like `OutOfMemoryError` that should typically cause the application to exit.

Instead of catching broad exception types, identify the specific exceptions that can occur and handle them appropriately. This makes error handling more precise and prevents masking serious system-level problems.

**Example of problematic code:**
```java
try {
    compressedPayload = ClientTelemetryUtils.compress(payload, compressionType);
} catch (Throwable e) {
    log.debug("Failed to compress telemetry payload for compression: {}, sending uncompressed data", compressionType);
    // This catches OutOfMemoryError, which should probably crash the JVM
}
```

**Improved approach:**
```java
try {
    compressedPayload = ClientTelemetryUtils.compress(payload, compressionType);
} catch (IOException | NoClassDefFoundError e) {
    log.debug("Failed to compress telemetry payload for compression: {}, sending uncompressed data", compressionType, e);
    // Only catches the specific exceptions we can recover from
}
```

When you must catch broader exception types, document why and consider whether the error handling is appropriate for all possible exception types that could be caught. Remember that catching `Throwable` would catch things like `OutOfMemoryException` and various other exceptions that indicate the JVM should exit.