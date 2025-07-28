---
title: prefer let-else patterns
description: When handling Option types that require early returns on None values,
  prefer the let-else pattern over verbose match statements or if-let constructs.
  This pattern improves code readability, reduces nesting, and makes the control flow
  more explicit.
repository: helix-editor/helix
label: Null Handling
language: Rust
comments_count: 6
repository_stars: 39026
---

When handling Option types that require early returns on None values, prefer the let-else pattern over verbose match statements or if-let constructs. This pattern improves code readability, reduces nesting, and makes the control flow more explicit.

The let-else pattern allows you to destructure an Option and immediately return or continue execution if the value is None, keeping the happy path at the main indentation level.

**Prefer this:**
```rust
let Some(context) = context else {
    return;
};

let Some(capabilities) = self.capabilities.get() else {
    return false;
};

let Some(last) = values_rev.peek() else {
    return;
};
```

**Instead of this:**
```rust
if context.is_none() {
    return;
}
let context = context.as_deref().expect("context has value");

match self.capabilities.get() {
    Some(capabilities) => capabilities,
    None => return false,
};

let last = match values_rev.peek() {
    Some(last) => last,
    None => return,
};
```

This pattern is particularly effective for guard clauses and input validation, where you want to handle the None case immediately and continue with the Some value. It reduces cognitive load by eliminating nested scopes and makes the error handling path explicit and concise.