---
title: Readable Maintainable Code
description: 'Write Rust code so its intent is clear at a glance and responsibilities
  are placed correctly.


  Apply this checklist:

  - Remove redundant comments when the code is already self-explanatory.'
repository: aaif-goose/goose
label: Code Style
language: Rust
comments_count: 5
repository_stars: 51876
---

Write Rust code so its intent is clear at a glance and responsibilities are placed correctly.

Apply this checklist:
- Remove redundant comments when the code is already self-explanatory.
- Keep functions/logic in the module that owns the responsibility (avoid “leaking” unrelated behavior into unrelated files).
- Reduce duplicated branching: collapse overlapping `if edit && fork` / `else if` shapes into a single flow that reuses the right helper methods.
- Refactor hard-to-read expressions by introducing well-named intermediate variables.
- Replace “magic numbers” with named constants and prefer shared utilities over local re-implementations.

Example pattern for readability (intermediate variables + simplified conditions):
```rust
let requested_budget = thinking_budget_tokens(model_config);
let max_thinking_budget = max_tokens.saturating_sub(MIN_ANSWER_TOKENS);
let budget_tokens = requested_budget.min(max_thinking_budget);

if budget_tokens >= MIN_THINKING_BUDGET_TOKENS {
    // build the thinking config using budget_tokens
}
```