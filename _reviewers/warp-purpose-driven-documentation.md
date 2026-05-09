---
title: Purpose-Driven Documentation
description: When adding or modifying code, ensure comments/doc comments are written
  to explain meaning and rationale—not just what the code does or where it’s mutated.
repository: warpdotdev/warp
label: Documentation
language: Rust
comments_count: 6
repository_stars: 56893
---

When adding or modifying code, ensure comments/doc comments are written to explain meaning and rationale—not just what the code does or where it’s mutated.

Apply this checklist:
- **Explain “what” and “why”**: If behavior becomes more complex or non-obvious, update the associated doc comment to state the rationale (what problem it solves / why complexity changed).
- **Document invariants & ownership**: For fields/state, clarify the field’s meaning and why it exists (e.g., derived/non-canonical vs canonical), and note any expected lifecycle (when it can be removed).
- **Keep comments attached**: Don’t insert unrelated items (e.g., `#[cfg]` helpers) between a doc comment and the item it documents; structure code so the comment clearly binds to the intended symbol.
- **Avoid ambiguous references**: In user-facing or accessibility text, use specific nouns (e.g., the actual tab name) rather than vague pronouns like “this tab.”
- **Justify non-obvious decisions**: For intentional exceptions or UI/logic branches, include short “why” comments to prevent future regressions.

Example (clarifying non-canonical state intent):
```rust
/// Current known statuses as reported to clients.
/// Not the canonical source of truth; once canonical indexing state is wired in,
/// this transitional cache should be removed.
codebase_index_statuses_by_repo: HashMap<String, RemoteCodebaseIndexStatus>,
```