---
title: Redact sensitive credentials
description: When implementing authentication or handling credentials, always redact
  sensitive information (keys, tokens, passwords) in logs and debug output. Using
  placeholder text like "<redacted>" or obfuscation techniques ensures credentials
  aren't accidentally exposed through logs, which could lead to security breaches.
repository: pola-rs/polars
label: Security
language: Rust
comments_count: 1
repository_stars: 34296
---

When implementing authentication or handling credentials, always redact sensitive information (keys, tokens, passwords) in logs and debug output. Using placeholder text like "<redacted>" or obfuscation techniques ensures credentials aren't accidentally exposed through logs, which could lead to security breaches.

The example demonstrates using a mapping function to replace the actual credential content with a redacted placeholder:

```rust
if verbose {
    eprintln!(
        "[CloudOptions::build_azure]: azure_cli_account_key: {:?}",
        azure_cli_account_key.as_ref().map(|_| "<redacted>")
    );
}
```

This pattern ensures that even when debugging is enabled, sensitive credentials remain protected. Implementing this practice consistently across the codebase helps prevent accidental exposure of authentication details in log files, console output, or error reports that might be shared during troubleshooting.