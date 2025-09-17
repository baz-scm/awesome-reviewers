---
title: Validate before type conversions
description: Always validate input constraints and use safe conversion methods before
  performing type conversions that could fail or produce undefined behavior. Avoid
  arbitrary casting with `as` operators, especially when the source value range may
  not fit the target type.
repository: unionlabs/union
label: Null Handling
language: Rust
comments_count: 4
repository_stars: 74800
---

Always validate input constraints and use safe conversion methods before performing type conversions that could fail or produce undefined behavior. Avoid arbitrary casting with `as` operators, especially when the source value range may not fit the target type.

**Prefer safe conversion patterns:**
- Use `try_into().expect()` instead of `as` casting for fallible conversions
- Validate input constraints before conversion (e.g., array lengths, value ranges)
- Consider all possible input values when designing conversions

**Example of unsafe vs safe conversion:**
```rust
// Unsafe - arbitrary casting without validation
let raw = val.to_le_bytes()[0];
let status = Status::try_from(raw as u32)?;

// Safe - validate constraints and use proper error handling
let raw = val.to_le_bytes()[0];
let status = Status::try_from(raw)
    .map_err(|_| ContractError::InvalidClientStatusValue { value: raw })?;

// For address conversions - validate length first
if address_bytes.len() != 20 {
    return Err(eyre!("Invalid address length"));
}
let address = Address::new(address_bytes);
```

This prevents runtime panics, data corruption, and undefined behavior that can occur when conversions fail silently or when input constraints are violated.