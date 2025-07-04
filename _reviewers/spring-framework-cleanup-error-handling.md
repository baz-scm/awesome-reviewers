---
title: Cleanup error handling
description: When handling resources that require cleanup (like streams, connections,
  or transactions), ensure that errors during the cleanup phase don't overshadow or
  silently replace the original error. This applies to both try-with-resources and
  traditional try/finally blocks.
repository: spring-projects/spring-framework
label: Error Handling
language: Java
comments_count: 5
repository_stars: 58382
---

When handling resources that require cleanup (like streams, connections, or transactions), ensure that errors during the cleanup phase don't overshadow or silently replace the original error. This applies to both try-with-resources and traditional try/finally blocks.

Key practices:
1. For critical cleanup operations that might fail, catch and log errors rather than letting them propagate and possibly mask the original exception.
2. Use try-with-resources only when appropriate - consider whether exceptions from `close()` should be suppressed or logged.
3. When errors occur in cleanup phases of transactions or connection management, log them at an appropriate level but don't throw new exceptions.
4. Preserve the original cause when wrapping exceptions.

Example of good error handling during cleanup:

```java
// Handle errors in cleanup without losing original exception
Mono<Void> safeCleanupStep(String stepDescription, Mono<Void> stepMono) {
    if (!logger.isDebugEnabled()) {
        return stepMono.onErrorComplete();
    }
    return stepMono
        .doOnError(e -> logger.debug(String.format("Error ignored during %s: %s", 
                                                  stepDescription, e)))
        .onErrorComplete();
}

// Usage in transaction cleanup
if (shouldDoCleanup) {
    Mono<Void> step = safeCleanupStep("transaction cleanup", 
                                      cleanupOperation());
    afterCleanup = afterCleanup.then(step);
}
```

When using traditional try/finally blocks, explicitly catch and log exceptions in the finally block:

```java
InputStream in = null;
try {
    in = resource.getInputStream();
    // Process the stream...
    return result;
}
catch (Exception ex) {
    // Handle primary operation exception
    throw ex;
}
finally {
    if (in != null) {
        try {
            in.close();
        }
        catch (IOException ex) {
            // Log but don't throw to avoid masking original exception
            logger.warn("Error closing resource", ex);
        }
    }
}
```

Remember that try-with-resources doesn't silently swallow exceptions from close() methods - they're suppressed but attached to the primary exception, so choose this pattern carefully based on your error handling needs.