---
title: use descriptive names
description: Choose specific, purpose-revealing names that clearly communicate intent
  rather than generic, abbreviated, or ambiguous terms. Names should describe what
  something does or represents, not what it doesn't do.
repository: helix-editor/helix
label: Naming Conventions
language: Rust
comments_count: 7
repository_stars: 39026
---

Choose specific, purpose-revealing names that clearly communicate intent rather than generic, abbreviated, or ambiguous terms. Names should describe what something does or represents, not what it doesn't do.

**Examples of improvements:**
- Use `script_engine` instead of generic `engine` to clarify the file's purpose
- Use `workspace_diagnostics` instead of abbreviated `w_diagnostics` for clarity  
- Use `shush` instead of `noop` when the function has side effects (not truly a no-op)
- Describe functionality positively: "Only show filename" instead of "Don't expand filenames"
- Use `variables::expand()` instead of `expand_args()` to be clearer about what it operates on

**Apply this by:**
- Asking "Does this name clearly explain the purpose/behavior?" when naming functions, variables, modules, and types
- Avoiding generic terms like `engine`, `handler`, `manager` without qualifying context
- Preferring full words over abbreviations in public APIs and important identifiers
- Using positive descriptions that state what something does rather than what it doesn't do
- Ensuring names remain unambiguous even when used in different contexts

This principle improves code readability and reduces the cognitive load for developers trying to understand unfamiliar code.