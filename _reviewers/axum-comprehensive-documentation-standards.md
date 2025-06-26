---
title: "Comprehensive documentation standards"
description: "Create clear, well-structured API documentation following proper formatting, correct references, informative examples, and completeness standards. Documentation should be treated as a first-class feature - it's often the first interaction users have with your API."
repository: "tokio-rs/axum"
label: "Documentation"
language: "Rust"
comments_count: 16
repository_stars: 22100
---

Create clear, well-structured API documentation following these practices:

1. **Use proper formatting**:
   - Separate distinct thoughts with blank lines
   - Ensure consistent paragraph structure
   - Add proper spacing after section headers

```rust
/// Create a multipart form to be used in API responses.
///
/// This struct implements [`IntoResponse`], and so it can be returned from a handler.
```

2. **Use correct references**:
   - Place code elements in backticks with proper linking: [`Type`] not `Type` or Type
   - Use intra-doc links for internal references: `[order-of-extractors]: crate::extract#the-order-of-extractors`
   - Specify version requirements when applicable: "This macro is only available with Rust >= 1.80"

3. **Write informative examples**:
   - Implement documentation tests where possible: `#[doc(test)]`
   - Include complete, runnable code examples
   - Add explanatory comments for complex operations
   - Format examples consistently with proper spacing

4. **Ensure completeness**:
   - Document security implications of sensitive operations
   - Clarify parameter constraints and return value behaviors
   - Use precise language: "This allows sharing state with `IntoResponse` implementations" not "This allows sharing state with IntoResponse implementations"
   - Add trailing periods to documentation sentences

Documentation should be treated as a first-class feature - it's often the first interaction users have with your API.