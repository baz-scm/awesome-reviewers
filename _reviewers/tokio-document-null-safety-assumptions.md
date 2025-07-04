---
title: Document null safety assumptions
description: When writing code that handles potentially null, undefined, or uninitialized
  values, always document safety assumptions with clear comments. This is especially
  important for unsafe blocks that manipulate raw pointers, uninitialized memory,
  or perform type conversions.
repository: tokio-rs/tokio
label: Null Handling
language: Rust
comments_count: 4
repository_stars: 28981
---

When writing code that handles potentially null, undefined, or uninitialized values, always document safety assumptions with clear comments. This is especially important for unsafe blocks that manipulate raw pointers, uninitialized memory, or perform type conversions.

Good safety comments should:
1. Explain why the operation is safe
2. Document preconditions that must be met
3. Clarify the expected state of variables
4. Mention any invariants being maintained

Example:

```rust
// BAD: Missing safety explanation
unsafe fn read_from<T: Read>(&mut self, rd: &mut T, max_buf_size: usize) -> io::Result<usize> {
    let buf = &mut self.buf.spare_capacity_mut()[..max_buf_size];
    let buf = unsafe { &mut *(buf as *mut [MaybeUninit<u8>] as *mut [u8]) };
    let res = rd.read(buf);
    // ...
}

// GOOD: Clear safety documentation
/// Safety: `rd` must not read from the buffer passed to `read` and
/// must correctly report the length of the written portion of the buffer.
unsafe fn read_from<T: Read>(&mut self, rd: &mut T, max_buf_size: usize) -> io::Result<usize> {
    // SAFETY: The memory may be uninitialized, but `rd.read` will only write to the buffer.
    let buf = &mut self.buf.spare_capacity_mut()[..max_buf_size];
    let buf = unsafe { &mut *(buf as *mut [MaybeUninit<u8>] as *mut [u8]) };
    let res = rd.read(buf);
    // ...
}
```

When performing pointer casts or transmutes, be especially explicit about lifetime and ownership guarantees:

```rust
// GOOD: Clear pointer casting documentation
let inner: *mut InnerFuture<'static, T> = &mut self.0;
let inner: *mut InnerFuture<'_, T> = inner.cast();
// SAFETY: The future must not exist after the type `T` becomes invalid.
// This casts away the type-level lifetime check, but the inner future 
// never moves out of this structure, so it won't live longer than `T`.
let inner = unsafe { &mut *inner };
```

Proper documentation of safety assumptions helps prevent subtle bugs, assists future maintainers, and makes code auditing more effective.