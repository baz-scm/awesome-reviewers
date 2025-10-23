---
title: avoid unwrap and panic
description: 'Replace `.unwrap()` and `panic!()` calls with proper error handling
  to prevent crashes and improve robustness. When encountering potential failures,
  choose one of three approaches:'
repository: servo/servo
label: Error Handling
language: Rust
comments_count: 9
repository_stars: 32962
---

Replace `.unwrap()` and `panic!()` calls with proper error handling to prevent crashes and improve robustness. When encountering potential failures, choose one of three approaches:

1. **Propagate the error** to the caller using `Result` types
2. **Log and continue** with graceful degradation 
3. **Use `.expect()`** with clear, actionable messages if crashing is truly intended

**Examples:**

Instead of:
```rust
let result = receiver.recv().unwrap().unwrap();
```

Use propagation:
```rust
fn get_result(&self) -> Result<SomeType, Error> {
    let result = receiver.recv().map_err(|e| Error::IpcFailure)?
        .map_err(|e| Error::OperationFailed)?;
    Ok(result)
}
```

Instead of:
```rust
devtools_chan.send(msg).unwrap();
```

Use logging:
```rust
if let Err(e) = devtools_chan.send(msg) {
    log::error!("DevTools send failed: {e}");
}
```

Instead of:
```rust
let components = string.split('x').collect::<Vec<_>>();
Ok(Some(Size2D::new(components[0], components[1])))
```

Use graceful handling:
```rust
let (width, height) = string.split_once('x')
    .ok_or(ParseResolutionError::InvalidFormat)?;
```

This approach prevents unexpected crashes, especially in content processes, and provides better debugging information when failures occur.