---
title: reduce complexity for readability
description: Prioritize code readability by reducing complexity through better organization
  and clearer patterns. Use early returns to avoid deep nesting, extract methods to
  break down large functions, and choose appropriate data structures over generic
  ones.
repository: servo/servo
label: Code Style
language: Rust
comments_count: 20
repository_stars: 32962
---

Prioritize code readability by reducing complexity through better organization and clearer patterns. Use early returns to avoid deep nesting, extract methods to break down large functions, and choose appropriate data structures over generic ones.

Key practices:
- **Use early returns** to reduce nesting levels instead of deeply nested if-else chains
- **Extract methods** when functions become large or handle multiple responsibilities  
- **Replace tuples with named structs** when multiple values need to be distinguished
- **Prefer idiomatic patterns** like `match` expressions and iterator methods over manual loops
- **Remove unnecessary abstractions** like builder patterns when they don't add value

Example of improving nested code:
```rust
// Instead of deep nesting:
if ancestor.is::<Document>() {
    true
} else if ancestor.is::<Element>() {
    let ancestor = ancestor.downcast::<Element>().unwrap();
    // ... complex logic
} else {
    false
}

// Use early returns:
if ancestor.is::<Document>() {
    return true;
}
let Some(ancestor) = ancestor.downcast::<Element>() else {
    return false;
};
// ... simplified logic
```

This approach makes code easier to follow, test, and maintain by reducing cognitive load and making the control flow more explicit.