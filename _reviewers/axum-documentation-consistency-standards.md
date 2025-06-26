---
title: "Documentation consistency standards"
description: "Maintain consistent documentation formatting standards across all project files, especially in changelogs, code examples, and technical documentation. This ensures readability and prevents confusion when documentation is viewed in different contexts."
repository: "tokio-rs/axum"
label: "Documentation"
language: "Markdown"
comments_count: 5
repository_stars: 22100
---

Maintain consistent documentation formatting standards across all project files, especially in changelogs, code examples, and technical documentation. This ensures readability and prevents confusion when documentation is viewed in different contexts.

Key practices to follow:
1. Use consistent formatting for PR references in changelogs - always use parentheses for PR references `([#123])` and include reference links at the bottom of the file
2. Format code elements with backticks in markdown text (e.g., `IntoResponse`, `FromRequest`)
3. Format code examples to clearly demonstrate the intended API usage:
```rust
// GOOD: Clear method chaining that shows which method calls apply to which objects
let app = Router::new().route(
    "/foo",
    get(|| async {})
        .route_layer(ValidateRequestHeaderLayer::bearer("password"))
);

// BAD: Confusing formatting that obscures the method call hierarchy
let app = Router::new()
    .route("/foo", get(|| async {})
    .route_layer(ValidateRequestHeaderLayer::bearer("password"))
);
```
4. Use proper Markdown link syntax consistently - either inline links `[text](url)` or reference-style links `[text][reference]` with the reference defined elsewhere, but not mixed approaches
5. Remember that documentation may be viewed outside GitHub (in editors, package documentation sites), where automatic linking doesn't work

Consistent documentation makes the codebase more approachable and reduces confusion for both contributors and users.