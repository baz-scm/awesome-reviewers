---
title: comprehensive API documentation
description: All public items, struct fields, and methods must have comprehensive
  documentation. When implementing web specifications, include the actual specification
  text in comments rather than just links, as specifications can change over time.
repository: servo/servo
label: Documentation
language: Rust
comments_count: 11
repository_stars: 32962
---

All public items, struct fields, and methods must have comprehensive documentation. When implementing web specifications, include the actual specification text in comments rather than just links, as specifications can change over time.

**Required Documentation:**
- All `pub` items must have rustdoc comments
- Struct fields should include purpose and links to relevant specifications
- Method return values and parameters must be explained
- Implementation steps should reference specification text

**Specification References:**
Include actual specification text in comments, not just links:

```rust
// ❌ Avoid link-only references
// Step 3 - 5.
// <https://w3c.github.io/webdriver/#dfn-deserialize-a-web-window>

// ✅ Include specification text
// Step 3: Let browsing context be the browsing context whose window handle is
// reference, or null if no such browsing context exists.
// Step 4: If browsing context is null or not a top-level browsing context,
// return error with error code no such window.
// Step 5: Return success with data browsing context's associated window.
```

**Comprehensive Field Documentation:**
```rust
// ✅ Document all fields with purpose and context
pub struct TextDecoderStream {
    reflector_: Reflector,
    /// Document-specific data required to fetch a web font.
    #[ignore_malloc_size_of = "Rc is hard"]
    decoder: Rc<TextDecoderCommon>,
    /// The associated transform, as per
    /// <https://streams.spec.whatwg.org/#generictransformstream>
    transform: Dom<TransformStream>,
}
```

This ensures code is self-documenting, maintainable, and provides clear context for future developers and specification compliance.