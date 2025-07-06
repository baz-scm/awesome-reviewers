---
title: Optimize algorithmic efficiency
description: 'Pay careful attention to operations inside loops and recursive functions
  to avoid unexpected algorithmic complexity. Be particularly vigilant about:


  1. **Hidden O(n²) operations**: Avoid operations that iterate over entire collections
  inside loops, as they can degrade performance significantly.'
repository: tokio-rs/tokio
label: Algorithms
language: Rust
comments_count: 4
repository_stars: 28981
---

Pay careful attention to operations inside loops and recursive functions to avoid unexpected algorithmic complexity. Be particularly vigilant about:

1. **Hidden O(n²) operations**: Avoid operations that iterate over entire collections inside loops, as they can degrade performance significantly.

```rust
// Poor performance: iterates through all buffers on each call
let n = bufs.iter().map(|b| b.len()).sum::<usize>().min(MAX_BUF);

// Better approach: avoid recomputing the total length repeatedly
let mut total = 0;
for buf in bufs {
    total += buf.len();
    if total >= MAX_BUF {
        total = MAX_BUF;
        break;
    }
}
```

2. **Prefer efficient bit operations**: Use shifts, masks, and other bit-level operations instead of more expensive calculations when possible.

```rust
// Expensive calculation using power
let max_number = 2u64.saturating_pow((8 * length_field_len - 1) as u32);
max_number + (max_number - 1);

// More efficient using bit shift
let max_number = match 1.checked_shl(8 * length_field_len) {
    Some(shl) => shl - 1,
    None => u64::MAX,
}
```

3. **Reduce monomorphization bloat**: Extract type-independent logic into separate functions to avoid code duplication across different type instantiations.

```rust
// Separate logic into non-generic helper function
pub(crate) fn spawn_child_with(
    cmd: &mut StdCommand,
    with: impl Fn(&mut StdCommand) -> io::Result<StdChild>,
) -> io::Result<SpawnedChild> {
    spawn_child(&mut with(cmd)?)
}

fn spawn_child(cmd: &mut StdChild) -> io::Result<SpawnedChild> {
    // Common implementation that won't be duplicated
}
```

4. **Use specialized methods**: Many standard library types offer specialized methods that are more efficient than general-purpose approaches.

```rust
// Less efficient with multiple operations
if now > timeout.checked_add(Duration::from_millis(5)).unwrap_or_else(Instant::far_future) {
    // Handle case
}

// More efficient using a specialized method
if now.saturating_duration_since(timeout) > Duration::from_millis(5) {
    // Handle case
}
```

These optimizations matter most in hot code paths, libraries meant for wide adoption, or when handling large data structures.