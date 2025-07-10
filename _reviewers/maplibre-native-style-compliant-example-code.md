---
title: Style-compliant example code
description: Example code in documentation and tutorials should adhere to project
  style guidelines and demonstrate best practices. Avoid using internal classes or
  implementation details that are inaccessible to users. Instead, use public APIs
  and concrete resources that developers can directly copy into their applications.
repository: maplibre/maplibre-native
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 1411
---

Example code in documentation and tutorials should adhere to project style guidelines and demonstrate best practices. Avoid using internal classes or implementation details that are inaccessible to users. Instead, use public APIs and concrete resources that developers can directly copy into their applications.

For instance, instead of using test-specific utilities:
```kotlin
this.maplibreMap.setStyle(
    Style.Builder().fromUri(TestStyles.getPredefinedStyleWithFallback("Streets"))
)
```

Use concrete, accessible resources:
```kotlin
this.maplibreMap.setStyle(
    Style.Builder().fromUri("https://demotiles.maplibre.org/style.json")
)
```

Similarly, when demonstrating architecture patterns (like in SwiftUI), follow established best practices even if they require additional complexity. Since developers often copy example code directly into their projects, prioritize teaching proper patterns over shortcuts. This principle extends to all examples regardless of language or framework—always prefer clarity, correctness, and adherence to project style guidelines over brevity.