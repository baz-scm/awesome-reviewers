---
title: "Axum Code Review: Interaction Patterns"
description: "When implementing Axum-based applications, it is crucial to ensure that the interaction patterns between components are well-designed and clearly documented. This includes understanding edge cases, limitations, and best practices around state sharing, router nesting, and extractor ordering."
repository: "tokio-rs/axum"
label: "Axum"
language: "TypeScript"
comments_count: 9
repository_stars: 22100
---

When implementing Axum-based applications, it is crucial to ensure that the interaction patterns between components are well-designed and clearly documented. This includes understanding edge cases, limitations, and best practices around state sharing, router nesting, and extractor ordering.

For nested routers, be sure to explicitly document how fallbacks work between the nested components. Provide clear examples showing the order in which fallbacks are handled for different paths.

When using extractors, clearly specify the ordering constraints and provide complete, working examples to demonstrate the correct usage. Extractors that consume the request body must be ordered last.

Carefully consider state sharing mechanisms between routers. Explain how states are merged or propagated, and explicitly note any limitations. This will help other developers avoid common pitfalls when integrating your Axum-based components.

By providing this level of detail and guidance, you can help ensure that developers working with your Axum-based code can understand critical interactions and implement them correctly, avoiding common issues and improving the overall quality and maintainability of the application.