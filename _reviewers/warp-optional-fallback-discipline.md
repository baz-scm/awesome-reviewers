---
title: Optional Fallback Discipline
description: 'When working with nullable/optional values or external/runtime-provided
  fields, never assume presence or a specific concrete type/spelling. Instead: (1)
  explicitly treat inputs as optional, (2) provide deterministic fallbacks (often
  empty string/None/previous-state), (3) avoid dereferencing missing values, and (4)
  add tests for both “value present” and...'
repository: warpdotdev/warp
label: Null Handling
language: Markdown
comments_count: 2
repository_stars: 56893
---

When working with nullable/optional values or external/runtime-provided fields, never assume presence or a specific concrete type/spelling. Instead: (1) explicitly treat inputs as optional, (2) provide deterministic fallbacks (often empty string/None/previous-state), (3) avoid dereferencing missing values, and (4) add tests for both “value present” and “value absent / alternate field present” cases.

Apply this especially to:
- UI state: preserve the existing focus target if one exists (it may not be terminal input); don’t hardcode a single focus type.
- Runtime metadata/env fields: probe multiple possible field names across versions and fall back safely when neither exists.
- Generated values: when a field is unavailable, emit a safe inert default (e.g., `""`) rather than constructing partial commands/paths.

Example (runtime field fallback):
```rust
fn nu_home_path(env: &HashMap<String, String>) -> String {
    // Prefer $nu.home-path when exposed; fall back to $nu.home-dir, then finally $HOME.
    env.get("nu.home-path")
        .or_else(|| env.get("nu.home-dir"))
        .or_else(|| env.get("HOME"))
        .cloned()
        .unwrap_or_else(|| "".to_string())
}
```

Checklist for PRs:
- Are any runtime/API/UI-derived values optional? If yes, are they handled with fallbacks (not assumptions)?
- Are there tests that cover absence and alternate-field spelling/runtime versions?
- Does the code avoid “half-built” outputs when values are missing (e.g., empty string/inert output instead of null or malformed command text)?