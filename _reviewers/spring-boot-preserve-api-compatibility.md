---
title: Preserve API compatibility
description: 'When evolving APIs, maintain backward compatibility to avoid breaking
  client code. Consider these guidelines:


  1. **Add overloaded methods instead of modifying signatures**: When adding parameters,
  create a new method rather than changing an existing one.'
repository: spring-projects/spring-boot
label: API
language: Java
comments_count: 9
repository_stars: 77637
---

When evolving APIs, maintain backward compatibility to avoid breaking client code. Consider these guidelines:

1. **Add overloaded methods instead of modifying signatures**: When adding parameters, create a new method rather than changing an existing one.

```java
// AVOID: Breaking change by modifying existing method
- public DockerConfiguration withHost(String address, boolean secure, String certificatePath) {
+ public DockerConfiguration withHost(String address, boolean secure, String certificatePath, Integer socketTimeout) {

// PREFER: Add an overloaded method
public DockerConfiguration withHost(String address, boolean secure, String certificatePath) {
    return withHost(address, secure, certificatePath, null);
}

public DockerConfiguration withHost(String address, boolean secure, String certificatePath, Integer socketTimeout) {
    // Implementation
}
```

2. **Use more general types when specializing parameters**: When changing parameter types, prefer changes that won't break existing code:

```java
// AVOID: Breaking change by narrowing type
- protected Function<String, String> getDefaultValueResolver(Environment environment) {
+ protected UnaryOperator<String> getDefaultValueResolver(Environment environment) {

// PREFER: Keep compatible types or provide adaptation layer
protected Function<String, String> getDefaultValueResolver(Environment environment) {
    // Implementation
}
```

3. **For functional interfaces, avoid changing the abstract method signature**: This preserves lambda compatibility.

4. **When breaking changes are unavoidable**:
   - Deprecate the old API first with clear migration notes
   - Keep both implementations for at least one release cycle
   - Provide automated migration tooling if possible

5. **Expand types to be more inclusive rather than restrictive**: Consider future use cases when designing parameter types:

```java
// AVOID: Restrictive single value
private String audience;

// PREFER: More flexible collection that handles current and future cases
private List<String> audiences;
```

These practices help maintain a stable API contract while allowing your library to evolve.