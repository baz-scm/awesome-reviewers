---
title: Follow import style
description: 'Tokio projects follow specific import conventions for consistency and
  readability. Adhere to these guidelines:


  1. Use separate `use` statements for different modules'
repository: tokio-rs/tokio
label: Code Style
language: Rust
comments_count: 6
repository_stars: 28981
---

Tokio projects follow specific import conventions for consistency and readability. Adhere to these guidelines:

1. Use separate `use` statements for different modules
2. Group imports from the same module with braces
3. Don't use nested/grouped braces for imports from different modules
4. Place safety comments directly before unsafe blocks

```rust
// Incorrect
use std::{
    future::Future,
    os::unix::io::{AsRawFd, RawFd},
};

// Correct
use std::future::Future;
use std::os::unix::io::{AsRawFd, RawFd};

// Incorrect - safety comment is too far from unsafe block
let filled = read.filled().len();
// Safety: This is guaranteed by invariants...
unsafe { pin.rd.advance_mut(filled) };

// Correct
// Safety: This is guaranteed by invariants...
unsafe { pin.rd.advance_mut(read.filled().len()) };
```

Following consistent import style and proper safety comment placement improves code readability and maintainability across the project.