---
title: API type consistency
description: Use structured types instead of generic strings in API definitions to
  improve type safety and clarity. Prefer enums over string literals, specific ID
  types over generic strings, and maintain consistent data type usage across request/response
  models.
repository: juspay/hyperswitch
label: API
language: Rust
comments_count: 7
repository_stars: 34028
---

Use structured types instead of generic strings in API definitions to improve type safety and clarity. Prefer enums over string literals, specific ID types over generic strings, and maintain consistent data type usage across request/response models.

Key practices:
- Use enum types for status fields instead of strings: `pub status: SubscriptionStatus` not `pub status: String`
- Use specific ID types: `merchant_id: impl Into<id_type::MerchantId>` not `merchant_id: String`
- Use connector enums: `connector: Connector` not `connector: String`
- Maintain URL validation with proper types: `base_url: Url` not `base_url: String`
- Use consistent amount types (MinorUnit vs StringMajorUnit) based on context

Example:
```rust
// Good - structured types
#[derive(Debug, Clone, serde::Serialize)]
pub struct CreateSubscriptionResponse {
    pub status: SubscriptionStatus,  // enum instead of String
    pub merchant_id: id_type::MerchantId,  // specific ID type
    pub connector: Connector,  // enum instead of String
}

// Avoid - generic strings
pub struct CreateSubscriptionResponse {
    pub status: String,  // unclear what values are valid
    pub merchant_id: String,  // loses type safety
    pub connector: String,  // no validation
}
```

This approach prevents runtime errors, improves API documentation, enables better IDE support, and makes the codebase more maintainable.