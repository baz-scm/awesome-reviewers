---
title: API boundary null handling
description: 'Establish consistent null handling patterns at API boundaries to prevent
  null pointer exceptions and improve code clarity:


  1. Validate method parameters using explicit null checks:'
repository: spring-projects/spring-framework
label: Null Handling
language: Java
comments_count: 5
repository_stars: 58382
---

Establish consistent null handling patterns at API boundaries to prevent null pointer exceptions and improve code clarity:

1. Validate method parameters using explicit null checks:
```java
public void setHttpClient(HttpClient httpClient) {
    Assert.notNull(httpClient, "HttpClient must not be null");
    this.httpClient = httpClient;
}
```

2. Return empty collections instead of null:
```java
public List<PropertyAccessor> getPropertyAccessors() {
    return Collections.emptyList();  // Instead of returning null
}
```

3. Use Optional only as a return type, never as a field:
```java
// DON'T
private Optional<HttpStatus> errorStatus;  // Avoid Optional as field

// DO
public Optional<User> findUserById(String id) {  // OK as return type
    // ...
}
```

4. For nullable return values in internal APIs, prefer explicit @Nullable annotation over Optional:
```java
@Nullable
protected Class<?> getReturnType(Method method) {
    // ...
}
```

These patterns ensure consistent null handling, improve code readability, and reduce the likelihood of null-related bugs. They also help maintain clear contracts between components while avoiding unnecessary Optional usage.