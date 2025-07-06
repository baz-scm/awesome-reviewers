---
title: Reuse test patterns
description: Minimize duplication and improve test maintainability by reusing existing
  test patterns and leveraging parameterization. When testing similar functionality
  across modules or with varying inputs, prefer adapting existing test cases and using
  parameterized tests over creating entirely new test files.
repository: quarkusio/quarkus
label: Testing
language: Java
comments_count: 3
repository_stars: 14667
---

Minimize duplication and improve test maintainability by reusing existing test patterns and leveraging parameterization. When testing similar functionality across modules or with varying inputs, prefer adapting existing test cases and using parameterized tests over creating entirely new test files.

For multiple test cases with similar structure but different inputs, use `@ParameterizedTest`:

```java
@ParameterizedTest
@ValueSource(strings = {"GraalVM CE 26-dev+1.1", "GraalVM CE 25-dev+26.1", "GraalVM CE 24.0.1+9.1"})
public void testGraalVMRuntimeVersion(String versionString) {
    System.setProperty(GRAALVM_VENDOR_VERSION_PROP, versionString);
    io.quarkus.runtime.graal.GraalVM.Version v = io.quarkus.runtime.graal.GraalVM.Version.getCurrent();
    // Assertions specific to each version can use parameters too
}
```

When implementing tests for a module, look for existing tests in related modules that cover similar functionality. For example, when adding tests for Hibernate Reactive's multi-persistence units:

```java
// Instead of creating entirely new test scenarios
// Look at existing tests that can be adapted:
// e.g., from extensions/hibernate-orm/deployment/src/test/java/io/quarkus/hibernate/orm/multiplepersistenceunits
```

This approach ensures testing consistency across the codebase, reduces maintenance overhead, and makes it easier to identify missing test coverage.