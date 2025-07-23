---
title: Document non-obvious aspects
description: Documentation should explain what isn't obvious from the code itself.
  Focus on providing context about "why" certain decisions were made rather than restating
  what the code does.
repository: openai/codex
label: Documentation
language: Rust
comments_count: 5
repository_stars: 31275
---

Documentation should explain what isn't obvious from the code itself. Focus on providing context about "why" certain decisions were made rather than restating what the code does.

Key practices:
- Explain non-obvious behavior or branching logic
- Document the purpose of tests, especially with complex setup
- Clarify what function return values represent
- Avoid comments that merely restate the code

**Good example:**
```rust
// Number of terminal rows consumed by the textarea border (top + bottom).
const TEXTAREA_BORDER_LINES: u16 = 2;
```

**Not as useful:**
```rust
// Render the main paragraph
paragraph.render_ref(area, buf);
```

When writing tests, include docstrings that explain what behavior is being verified, especially when the test involves complex setup code. For public functions, ensure return values are documented when their meaning isn't immediately clear from the function name or signature.