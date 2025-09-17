---
title: prioritize code clarity
description: Write code that prioritizes readability and explicitness over brevity.
  This includes using explicit type conversions instead of implicit ones, extracting
  magic values to named constants, creating helper functions for repetitive operations,
  and organizing code logic clearly.
repository: unionlabs/union
label: Code Style
language: Rust
comments_count: 10
repository_stars: 74800
---

Write code that prioritizes readability and explicitness over brevity. This includes using explicit type conversions instead of implicit ones, extracting magic values to named constants, creating helper functions for repetitive operations, and organizing code logic clearly.

Key practices:
- Use explicit conversions like `B256::from(raw_slot)` instead of `raw_slot.into()` for clarity
- Extract hardcoded values to named constants: `const CODE_OK: u32 = 0;` instead of inline `0`
- Create helper functions for repetitive operations rather than duplicating complex logic
- Use direct, simple approaches like `.map()` instead of `.and_then(|s| Some(s))`
- Pull complex conditional logic out of control flow guards for better readability
- Prefer `.is_ok()` over pattern matching `Ok(_)` when the value isn't used

Example of improving clarity:
```rust
// Before: implicit conversion and magic number
let raw_slot: B256 = raw_slot.into();
if tx.tx_result.code == 0 {

// After: explicit conversion and named constant  
const CODE_OK: u32 = 0;
let raw_slot: B256 = B256::from(raw_slot);
if tx.tx_result.code == CODE_OK {
```

This approach makes code more maintainable, reduces cognitive load for reviewers, and prevents subtle bugs from unclear operations.