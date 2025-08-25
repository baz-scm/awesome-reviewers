---
title: avoid concurrency anti-patterns
description: Avoid common concurrency anti-patterns that lead to race conditions,
  deadlocks, and unreliable behavior. Use structured approaches instead of ad-hoc
  solutions.
repository: block/goose
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 19037
---

Avoid common concurrency anti-patterns that lead to race conditions, deadlocks, and unreliable behavior. Use structured approaches instead of ad-hoc solutions.

**Key anti-patterns to avoid:**
1. **Manual buffer management with select!** - Can cause race conditions where data is lost
2. **Sleep-based synchronization** - Creates timing dependencies and potential bugs
3. **Wrong synchronization primitives** - Using Mutex when RwLock is needed blocks concurrent readers
4. **Improper lock lifetime management** - Forgetting to release locks can cause deadlocks

**Preferred approaches:**
- Use streams for async data processing instead of manual buffer handling
- Choose RwLock over Mutex when multiple concurrent readers are expected
- Explicitly manage lock lifetimes with `drop()` when needed
- Avoid timing-based solutions like sleep delays for synchronization

**Example:**
```rust
// Anti-pattern: Manual buffer management with select!
select! {
    n = stdout_reader.read_until(b'\n', &mut stdout_buf) => {
        // Risk of losing last chunk of data
    }
}

// Better: Use streams
let stdout_stream = LinesStream::new(BufReader::new(stdout).lines());
let stderr_stream = LinesStream::new(BufReader::new(stderr).lines());
// Drive streams to completion without manual buffer management

// Anti-pattern: Wrong lock type
pub(super) extension_manager: Mutex<ExtensionManager>, // Blocks concurrent readers

// Better: Allow concurrent reads
pub(super) extension_manager: RwLock<ExtensionManager>, // Multiple readers, single writer
```