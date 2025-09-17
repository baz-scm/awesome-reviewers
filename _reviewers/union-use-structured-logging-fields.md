---
title: Use structured logging fields
description: Prefer structured logging fields over string formatting in tracing logs
  to improve searchability, parsing, and consistency. Use field syntax like `field
  = %value` or `%field` instead of embedding values directly in log messages. Keep
  log messages single-line, lowercase, and include relevant context as separate fields.
repository: unionlabs/union
label: Logging
language: Rust
comments_count: 4
repository_stars: 74800
---

Prefer structured logging fields over string formatting in tracing logs to improve searchability, parsing, and consistency. Use field syntax like `field = %value` or `%field` instead of embedding values directly in log messages. Keep log messages single-line, lowercase, and include relevant context as separate fields.

**Examples:**

Instead of:
```rust
tracing::info!("SendPacket event recorded for sequence {}. key: {}", sequence, key);
tracing::info!("ETH Token balance: {}. Sending amount: {}", balance, amount);
debug!("abi build log: \n-----------\n{}\n-----------", log);
```

Use:
```rust
tracing::info!(sequence = %sequence, key = %key, "sendpacket event recorded");
tracing::info!(balance = %balance, amount = %amount, "eth token balance check");
debug!(stdout = %output.stdout, stderr = %output.stderr, "abi build log");
```

This approach makes logs more structured, easier to query, and maintains consistency across the codebase. Always include relevant contextual information like chain IDs, block numbers, addresses, and amounts as separate fields rather than formatting them into the message string.