---
title: Organize code structure
description: Maintain clean and well-organized code structure by following consistent
  organizational patterns. This improves readability, maintainability, and reduces
  cognitive load for developers.
repository: juspay/hyperswitch
label: Code Style
language: Rust
comments_count: 15
repository_stars: 34028
---

Maintain clean and well-organized code structure by following consistent organizational patterns. This improves readability, maintainability, and reduces cognitive load for developers.

Key practices to follow:

1. **Import Organization**: Place all imports at the top of files and avoid wildcard imports
```rust
// Good
use common_enums::enums;
use hyperswitch_domain_models::payment_method_data::PaymentMethodData;

// Avoid
use crate::hyperswitch_ai_interaction::*;
use masking::ExposeOptionInterface; // Move to top
```

2. **Functional Organization**: Group related functionality together and place code in appropriate modules
```rust
// Move validation logic to validator.rs
// Keep type transformations in transformers.rs  
// Place constants in dedicated const files or appropriate modules
```

3. **Eliminate Code Duplication**: Extract common logic into shared functions rather than duplicating implementations
```rust
// Instead of separate v1/v2 functions with identical logic
pub fn common_method() -> Result<Self, Error> {
    // shared implementation
}
```

4. **Use Explicit Patterns**: Avoid wildcard matching and imports for better code clarity
```rust
// Good
match token_data {
    storage::PaymentTokenData::TemporaryGeneric(token) => { /* ... */ }
    storage::PaymentTokenData::PermanentCard(card) => { /* ... */ }
}

// Avoid
match token_data {
    storage::PaymentTokenData::TemporaryGeneric(token) => { /* ... */ }
    _ => { /* ... */ }
}
```

5. **Remove Unnecessary Code**: Clean up unused variables, commented code blocks, and unnecessary utility functions that duplicate existing functionality.

This organizational approach ensures code remains maintainable as the codebase grows and makes it easier for team members to locate and understand functionality.