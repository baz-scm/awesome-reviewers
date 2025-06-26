---
title: "Minimize memory allocation overhead"
description: "Optimize performance by minimizing unnecessary memory allocations and using allocation-efficient APIs. Key practices include using static data when possible instead of dynamic allocations, leveraging specialized types and methods that minimize copies, and considering allocation patterns in data transformations."
repository: "tokio-rs/axum"
label: "Performance Optimization"
language: "Rust"
comments_count: 4
repository_stars: 22100
---

Optimize performance by minimizing unnecessary memory allocations and using allocation-efficient APIs. Key practices:

1. Use static data when possible instead of dynamic allocations
2. Leverage specialized types and methods that minimize copies
3. Consider allocation patterns in data transformations

Example - Before:
```rust
// Unnecessary allocation
.send(Message::Ping("Hello, Server!".into()))

// Multiple potential allocations
let string = std::str::from_utf8(&bytes)
    .map_err(InvalidUtf8::from_err)?
    .to_owned();
```

Example - After:
```rust
// Using static data
.send(Message::Ping(Payload::Shared(
    "Hello, Server!".as_bytes().into()
)))

// Direct conversion avoiding copies
let string = String::from_utf8(bytes.into())
    .map_err(InvalidUtf8::from_err)?;
```

For serialization/encoding operations, prefer methods that write directly to pre-allocated buffers rather than creating intermediate allocations. Consider using specialized types like BytesMut when working with byte buffers.