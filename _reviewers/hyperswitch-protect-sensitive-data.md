---
title: Protect sensitive data
description: Wrap all sensitive data fields in Secret<> types to prevent accidental
  exposure through logs, debug output, serialization, or error messages. This includes
  authentication tokens, API keys, PII data, payment information, and any credentials.
repository: juspay/hyperswitch
label: Security
language: Rust
comments_count: 8
repository_stars: 34028
---

Wrap all sensitive data fields in Secret<> types to prevent accidental exposure through logs, debug output, serialization, or error messages. This includes authentication tokens, API keys, PII data, payment information, and any credentials.

Fields that should be wrapped in Secret<>:
- Authentication tokens and API keys (access_token, client_secret, proxy_url)
- PII data (names, phone numbers, email addresses, social security numbers)
- Payment information (card numbers, bank account numbers, payment tokens)
- Internal identifiers that could be sensitive (vault IDs, processor tokens)

Example implementation:
```rust
// Instead of:
pub struct PaymentData {
    pub bank_number: Option<String>,
    pub client_secret: Option<String>,
    pub token: String,
}

// Use:
pub struct PaymentData {
    pub bank_number: Option<Secret<String>>,
    pub client_secret: Option<Secret<String>>,
    pub token: Secret<String>,
}
```

For highly sensitive data like KMS-encrypted tokens, consider additional encryption layers beyond the Secret<> wrapper. The Secret<> type prevents accidental logging and provides controlled access through methods like `expose()` or `peek()`, ensuring sensitive data is only accessed intentionally.