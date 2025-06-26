---
title: "Use Option combinators"
description: "Instead of verbose conditional logic, prefer Rust's Option combinators like map, and_then, and filter for handling potentially null values. This creates more concise, readable code that expresses intent clearly and reduces the chance of null-related bugs."
repository: "tokio-rs/axum"
label: "Null Handling"
language: "Rust"
comments_count: 4
repository_stars: 22100
---

Instead of verbose conditional logic, prefer Rust's Option combinators like `map`, `and_then`, and `filter` for handling potentially null values. This creates more concise, readable code that expresses intent clearly and reduces the chance of null-related bugs.

For example, replace:
```rust
let result = if let Some(value) = optional_value {
    Some(process(value))
} else {
    None
};
```

With:
```rust
let result = optional_value.map(process);
```

Similarly, when handling multiple optional values, use `and_then` instead of nested if-lets:
```rust
// Instead of this
let session_cookie =
    if let Ok(TypedHeader(cookie)) = TypedHeader::<Cookie>::from_request(req).await {
        cookie.get(AXUM_SESSION_COOKIE_NAME).map(|x| x.to_owned())
    } else {
        None
    };

// Prefer this
let session_cookie = Option::<TypedHeader<Cookie>>::from_request(req).await
    .and_then(|cookie| Some(cookie.get(AXUM_SESSION_COOKIE_NAME)?.to_owned()));
```

When validating values that might fail, explicitly set to None on failure:
```rust
self.filename = if let Ok(filename) = value.try_into() {
    Some(filename)
} else {
    trace!("Attachment filename contains invalid characters");
    None
};
```

Using Option combinators not only makes code more concise but also makes the intent clearer and reduces the chance of null-handling mistakes.