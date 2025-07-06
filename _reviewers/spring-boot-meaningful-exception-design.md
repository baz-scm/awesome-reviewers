---
title: Meaningful exception design
description: 'Design exceptions to provide clear context, preserve stack traces, and
  propagate correctly through your system. Key practices include:


  1. Choose the most appropriate exception type based on the error condition:'
repository: spring-projects/spring-boot
label: Error Handling
language: Java
comments_count: 6
repository_stars: 77637
---

Design exceptions to provide clear context, preserve stack traces, and propagate correctly through your system. Key practices include:

1. Choose the most appropriate exception type based on the error condition:
   - Use `IllegalArgumentException` for invalid inputs
   - Use `IllegalStateException` for invalid state
   - Avoid generic exceptions when more specific ones exist

```java
// Poor practice
throw new ValidationException("Cannot unwrap to " + type);

// Better practice
throw new IllegalArgumentException("Cannot unwrap " + target + " to " + type.getName());
```

2. Avoid unnecessary exception wrapping that obscures the original cause. Let original exceptions propagate when they provide sufficient context:

```java
// Unnecessary wrapping
try {
  this.jobLauncher.launch(job, jobParameters);
} catch (NoSuchJobException ex) {
  throw new JobExecutionException(ex.getMessage(), ex);
}

// Better approach - NoSuchJobException is already a JobExecutionException
// Remove the try/catch completely
this.jobLauncher.launch(job, jobParameters);
```

3. For cleanup operations during error handling, capture secondary failures as suppressed exceptions:

```java
catch (RuntimeException ex) {
  try {
    WebServer webServer = getWebServer();
    if (webServer != null) {
      webServer.stop();
    }
  }
  catch (Exception shutdownEx) {
    ex.addSuppressed(shutdownEx);
  }
  throw ex;
}
```

4. Prefer failing fast with specific exceptions when unexpected conditions occur rather than continuing with defensive fallbacks that might mask issues:

```java
// Defensive (might mask issues)
Method initializeMethod = ReflectionUtils.findMethod(this.tester, "initialize", Class.class, ResolvableType.class);
if (initializeMethod == null) {
  throw new IllegalStateException("unable to find initialize method for " + this.tester);
}

// Fail-fast (better for critical components)
Method initializeMethod = ReflectionUtils.findMethod(this.tester, "initialize", Class.class, ResolvableType.class);
// Let the NPE happen naturally if the method isn't found
```

5. Ensure proper error propagation in asynchronous contexts where traditional exception handling might not work:

```java
// Errors suppressed:
webClient.post()
  .bodyValue(body)
  .retrieve()
  .toBodilessEntity()
  .subscribe((__) -> {}, (__) -> {});

// Proper error handling:
webClient.post()
  .bodyValue(body)
  .retrieve()
  .toBodilessEntity()
  .subscribe((__) -> {}, (error) -> errorHandler.handleError(error));
```