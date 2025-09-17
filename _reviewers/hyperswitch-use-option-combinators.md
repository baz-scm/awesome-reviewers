---
title: use Option combinators
description: Leverage Rust's Option API methods like `map`, `and_then`, `is_some()`,
  and `filter` instead of manual pattern matching or nested conditional statements
  when working with optional values. This approach reduces code complexity, improves
  readability, and prevents common null-handling errors.
repository: juspay/hyperswitch
label: Null Handling
language: Rust
comments_count: 4
repository_stars: 34028
---

Leverage Rust's Option API methods like `map`, `and_then`, `is_some()`, and `filter` instead of manual pattern matching or nested conditional statements when working with optional values. This approach reduces code complexity, improves readability, and prevents common null-handling errors.

**Avoid manual checks:**
```rust
// Instead of this:
let is_there_an_active_payment_attempt_id = payment_intent.active_attempt_id.is_some();
if let Some(_customer_acceptance) = customer_acceptance {
    // nested logic
}

// Use Option combinators:
payment_intent.active_attempt_id.map(|attempt_id| {
    // handle the case when present
}).unwrap_or_else(|| {
    // handle the None case
});

// For simple existence checks:
if customer_acceptance.is_some() {
    // logic when present
}
```

**Chain operations safely:**
```rust
// Instead of nested match/if statements:
match connector_customer_id {
    Some(connector_customer_id) => {
        match update_token_expiry_based_on_schedule_time(state, &connector_customer_id, Some(s_time)).await {
            Ok(_) => {}
            Err(e) => { /* error handling */ }
        }
    }
    None => { /* log warning */ }
}

// Use Option methods:
connector_customer_id
    .map(|id| update_token_expiry_based_on_schedule_time(state, &id, Some(s_time)))
    .transpose()?
    .unwrap_or_else(|| logger::warn!("No connector customer id found"));
```

This pattern makes null safety explicit, reduces indentation levels, and leverages Rust's type system to prevent null reference errors at compile time.