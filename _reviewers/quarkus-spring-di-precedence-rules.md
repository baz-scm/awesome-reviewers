---
title: Spring DI precedence rules
description: When developing Quarkus extensions that interact with classes containing
  Spring annotations (like `@Service`, `@Component`, etc.), ensure your extension
  respects Spring DI's scope definitions by setting appropriate annotation transformer
  priorities.
repository: quarkusio/quarkus
label: Spring
language: Java
comments_count: 2
repository_stars: 14667
---

When developing Quarkus extensions that interact with classes containing Spring annotations (like `@Service`, `@Component`, etc.), ensure your extension respects Spring DI's scope definitions by setting appropriate annotation transformer priorities.

Spring DI extension uses the default priority of 1000 for its transformers. If your extension also adds scopes or bean-defining annotations to classes, it should use a lower priority value to allow Spring annotations to take precedence.

For example, when implementing an annotation transformer that adds scopes:

```java
@Override
public int priority() {
    return 500; // Lower priority than Spring DI's 1000
}
```

Alternatively, if using the `AutoAddScopeBuildItem` pattern:

```java
@BuildStep
AutoAddScopeBuildItem autoAddScope() {
   return AutoAddScopeBuildItem.builder()
      .containsAnnotations(YOUR_ANNOTATIONS) 
      .defaultScope(BuiltinScope.YOUR_SCOPE)
      .priority(500) // Lower than Spring DI's priority
      .build();
}
```

This approach prevents conflicts when multiple extensions try to add "auto" scopes to the same classes, ensuring Spring annotations are properly honored in the application.