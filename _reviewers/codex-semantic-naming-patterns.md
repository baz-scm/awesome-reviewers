---
title: Semantic naming patterns
description: Use names that clearly convey purpose and maintain consistency across
  related components. Avoid generic identifiers (like `dir`) in favor of descriptive
  ones (like `codex_home`), and ensure placeholder names in string templates are self-explanatory
  (prefer `SUMMARY_TEXT` over `{}`). For related functions or elements, establish
  consistent naming patterns...
repository: openai/codex
label: Naming Conventions
language: Rust
comments_count: 4
repository_stars: 31275
---

Use names that clearly convey purpose and maintain consistency across related components. Avoid generic identifiers (like `dir`) in favor of descriptive ones (like `codex_home`), and ensure placeholder names in string templates are self-explanatory (prefer `SUMMARY_TEXT` over `{}`). For related functions or elements, establish consistent naming patterns with meaningful symmetry, particularly for operations that are conceptually opposite.

When naming variables, functions, or constants:
1. Choose semantically rich names that reveal intent
2. Remove unnecessary prefixes for general-purpose elements (e.g., avoid `openai_request_max_retries` when it applies to all providers)
3. Ensure naming symmetry between related functions (if you have `fully_qualified_tool_name()`, its counterpart should be `parse_fully_qualified_tool_name()`)

Example:
```rust
// Poor naming
const TEMPLATE: &str = "Summary: {}";
fn get_name(s: &str, t: &str) -> String { /* ... */ }
fn extract(name: &str) -> (&str, &str) { /* ... */ }

// Better naming
const SUMMARY_TEMPLATE: &str = "Summary: {SUMMARY_TEXT}";
fn fully_qualified_tool_name(server: &str, tool: &str) -> String { /* ... */ }
fn parse_fully_qualified_tool_name(name: &str) -> (&str, &str) { /* ... */ }
```