---
title: optimize algorithmic efficiency
description: Eliminate unnecessary operations and choose appropriate data structures
  to improve algorithmic efficiency. Look for opportunities to remove redundant computations,
  avoid unnecessary allocations, and leverage built-in methods instead of manual implementations.
repository: alacritty/alacritty
label: Algorithms
language: Rust
comments_count: 10
repository_stars: 59675
---

Eliminate unnecessary operations and choose appropriate data structures to improve algorithmic efficiency. Look for opportunities to remove redundant computations, avoid unnecessary allocations, and leverage built-in methods instead of manual implementations.

Key areas to focus on:

1. **Remove unnecessary safety operations** when bounds are guaranteed. For example, avoid `saturating_sub` when the subtraction cannot underflow:
```rust
// Instead of this when bounds are guaranteed:
let middle_lines = total_lines.saturating_sub(1);

// Use this:
let middle_lines = total_lines - 1;
```

2. **Use built-in iterator methods** instead of manual iteration:
```rust
// Instead of manual zip:
for (p1, p2) in iter::zip(f_x, g_x) {

// Use built-in zip:
for (p1, p2) in f_x.zip(g_x) {
```

3. **Choose appropriate data structures** based on known constraints. Use fixed-size arrays instead of dynamic vectors when the maximum size is known and small:
```rust
// Instead of Vec for known small collections:
let uris: Vec<Vec<char>> = self.highlighted_hint.iter()...

// Consider fixed-size alternatives when applicable
```

4. **Avoid duplicate iterations** by combining operations or using more efficient algorithms:
```rust
// Instead of iterating twice to find byte and char indices:
if let Some(mut index) = self.state.find("://") {
    for (char_index, (byte_index, _)) in self.state.char_indices().enumerate() {
        if byte_index == index { index = char_index; break; }
    }

// Use char_indices directly with appropriate logic
```

5. **Simplify mathematical expressions** to reduce computational overhead and improve readability:
```rust
// Instead of complex division chains:
1_000_000 / (60_000 / 1000)

// Use simplified form:
1_000_000_000 / 60_000
```

6. **Optimize conditional logic** by restructuring boolean expressions for better performance and clarity:
```rust
// Instead of:
if uniq_hyperlinks.contains(&hyperlink) {
    return None;
}
uniq_hyperlinks.insert(hyperlink.clone());
Some((cell, hyperlink))

// Use:
if !uniq_hyperlinks.contains(&hyperlink) {
    uniq_hyperlinks.insert(hyperlink.clone());
    Some((cell, hyperlink))
} else {
    None
}
```

These optimizations improve both performance and code maintainability while reducing the likelihood of algorithmic inefficiencies.