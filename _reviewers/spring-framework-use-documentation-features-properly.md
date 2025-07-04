---
title: Use documentation features properly
description: 'Utilize Asciidoc features correctly when writing or updating Spring
  Framework documentation. Instead of hardcoded links, use defined attributes where
  available. For example, replace:'
repository: spring-projects/spring-framework
label: Documentation
language: Other
comments_count: 2
repository_stars: 58382
---

Utilize Asciidoc features correctly when writing or updating Spring Framework documentation. Instead of hardcoded links, use defined attributes where available. For example, replace:

```
[its `META-INF/spring.factories` properties file](https://github.com/spring-projects/spring-framework/blob/main/spring-test/src/main/resources/META-INF/spring.factories)
```

With:

```
[its `META-INF/spring.factories` properties file]{spring-framework-code}
```

When cross-referencing content within the same document, use simplified section references (e.g., `<<webflux>>` instead of `<<web/webflux.adoc#webflux>>`). This improves documentation consistency, maintainability, and reduces the effort needed for future updates. Proper use of Asciidoc features also helps maintain a consistent style across the entire codebase and makes documentation more resilient to structural changes.