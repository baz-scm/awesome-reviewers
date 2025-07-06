---
title: Secure unsafe code
description: 'When working with unsafe code, follow these practices to minimize security
  vulnerabilities:


  1. **Minimize scope**: Limit unsafe blocks to only the operations that require them.'
repository: tokio-rs/tokio
label: Security
language: Rust
comments_count: 4
repository_stars: 28989
---

When working with unsafe code, follow these practices to minimize security vulnerabilities:

1. **Minimize scope**: Limit unsafe blocks to only the operations that require them.
   ```rust
   // BAD: Overly broad unsafe block
   unsafe {
     let tail_block = &mut *tail;
     if tail_block.is_closed() { ... }
   }
   
   // GOOD: Minimal scope
   let tail_block = unsafe { &mut *tail };
   if tail_block.is_closed() { ... }
   ```

2. **Document safety**: Add a `// SAFETY:` comment above each unsafe block explaining why the operation is safe.
   ```rust
   // SAFETY: The pointer is guaranteed to be valid because it comes from an Arc
   // that we have exclusive access to via get_mut()
   unsafe { Arc::get_mut(&mut arc).unwrap_unchecked() }
   ```

3. **Isolate operations**: Use separate unsafe blocks for each unsafe operation.
   ```rust
   // BAD: Multiple unsafe operations in one block
   unsafe {
     let fd = syscall(SYS_pidfd_open, pid, PIDFD_NONBLOCK);
     if fd == -1 {
       let errno = *__errno_location();
       // ...
     }
   }
   
   // GOOD: Separate unsafe blocks
   let fd = unsafe { syscall(SYS_pidfd_open, pid, PIDFD_NONBLOCK) };
   if fd == -1 {
     let errno = unsafe { *__errno_location() };
     // ...
   }
   ```

4. **Encapsulate requirements**: Mark functions that expose unsafe requirements as unsafe themselves.
   ```rust
   // BAD: Function with hidden unsafe requirements
   pub fn read_from(&mut self, inner: &mut T) { ... }
   
   // GOOD: Properly marked function
   pub unsafe fn read_from(&mut self, inner: &mut T) { ... }
   ```

Following these practices helps prevent memory corruption vulnerabilities and makes unsafe code easier to audit and maintain.