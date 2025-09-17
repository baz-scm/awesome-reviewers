---
title: Use meaningful names
description: Use descriptive, self-explanatory names for variables, methods, fields,
  and types. Avoid single-letter variables, abbreviations, and generic naming that
  obscures intent.
repository: juspay/hyperswitch
label: Naming Conventions
language: Rust
comments_count: 17
repository_stars: 34028
---

Use descriptive, self-explanatory names for variables, methods, fields, and types. Avoid single-letter variables, abbreviations, and generic naming that obscures intent.

**Key principles:**
- Use descriptive variable names instead of single letters: `id_value` instead of `v`, `customer` instead of `c`
- Make method and field names self-explanatory: `mandate_type` instead of `action_type`, `is_sdk_client_token_generation_enabled` instead of `is_sdk_session_token_generation_enabled`
- Use domain-specific types instead of primitives: `id_type::CustomerId` instead of `String` for customer identifiers
- Use enums instead of string literals for categorical data: `AuthenticationStatus::Y` instead of `"Y"`
- Avoid redundant naming: use `client` instead of `superposition_client` when the struct name already indicates context
- Use constants for hardcoded values: `const ITEM_TYPE: &str = "plan"` instead of inline strings

**Example:**
```rust
// Poor naming
let c = &item.response.customer;
let n = c.name.as_ref().map(|n| n.clone().expose());
pub customer_id: String,
pub payment_method: String,

// Good naming  
let customer = &item.response.customer;
let customer_name = customer.name.as_ref().map(|name| name.clone().expose());
pub customer_id: id_type::CustomerId,
pub payment_method: PaymentMethodType,
```

Clear, meaningful names reduce cognitive load, improve code maintainability, and make the codebase more accessible to new developers.