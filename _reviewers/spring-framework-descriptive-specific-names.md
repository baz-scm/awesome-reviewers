---
title: Descriptive specific names
description: Choose names that are specific, descriptive, and accurately reflect the
  purpose and domain of variables, methods, classes, and constants. Avoid overly generic
  terms that could be ambiguous or conflict with future features.
repository: spring-projects/spring-framework
label: Naming Conventions
language: Java
comments_count: 8
repository_stars: 58382
---

Choose names that are specific, descriptive, and accurately reflect the purpose and domain of variables, methods, classes, and constants. Avoid overly generic terms that could be ambiguous or conflict with future features.

When naming constants, qualify them to avoid collisions:
```java
// Avoid
public static final String ATTRIBUTES_CHANNEL_KEY = "attributes";

// Prefer
public static final String ATTRIBUTES_CHANNEL_KEY = 
    ReactorClientHttpRequest.class.getName() + ".attributes";
```

For methods, use names that clearly describe their specific purpose:
```java
// Too generic
private PreparedStatementCallback<int[]> getPreparedStatementCallback(...) { }

// More descriptive
private PreparedStatementCallback<int[]> getPreparedStatementCallbackForBatchUpdate(...) { }
```

For parameters and variables, select names that accurately reflect their type and domain:
```java
// Potentially confusing (suggests java.nio.ByteBuffer)
public DataBuffer encodeValue(ByteBuf byteBuffer, ...) { }

// Clear and accurate
public DataBuffer encodeValue(ByteBuf byteBuf, ...) { }
```

When adding similar methods to existing APIs, choose names that align with established patterns:
```java
// Doesn't align with Optional's terminology
UriBuilder optionalQueryParam(String name, Optional<?> optionalValue);

// Aligns with terminology and sorts better alphabetically
UriBuilder queryParamIfPresent(String name, Optional<?> optionalValue);
```