---
title: Semantic, Contract-Revealing Names
description: 'Use naming that matches the code’s actual semantics and data contracts—avoid
  misleading terms and generic parameter names.


  Apply these rules:

  - Behavior-accurate wording: don’t use terms like “unset” when the implementation
  “restores”/“replaces” a previous value.'
repository: warpdotdev/warp
label: Naming Conventions
language: Rust
comments_count: 6
repository_stars: 56893
---

Use naming that matches the code’s actual semantics and data contracts—avoid misleading terms and generic parameter names.

Apply these rules:
- Behavior-accurate wording: don’t use terms like “unset” when the implementation “restores”/“replaces” a previous value.
- Domain-accurate nouns: if something isn’t a true “anchor”, don’t name APIs/vars “anchor”. Use the real concept (e.g., matching header).
- Contract-revealing identifiers: never name encoded/serialized inputs as just `value`; name the expected type/encoding.
- Terminology clarity: avoid vague or unexplained terms (e.g., “frame”) unless they’re widely recognized; otherwise reference the specific control/behavior, often via an enum with variants.
- User-facing terminology: ensure the vocabulary matches user understanding (e.g., prefer a single clear option like “none” rather than confusing “unset” vs “cleared”).

Example (pattern):
```rust
// Misleading: suggests truly removing state when we actually restore.
fn unset_warp_default(&mut self, ctx: &mut ModelContext<Self>) {
    self.restore_macos_terminal_as_default(ctx)
}

// Contract-revealing parameter names.
pub fn format_git_branch_command(encoded_branch: &str) -> String {
    // encoded_branch is a GitBranchOnClickValue-encoded string
    format!("git checkout {encoded_branch}")
}

// Domain-accurate API naming.
pub fn scroll_to_matching_header(&mut self, header: &str) { /* ... */ }

// Clear terminology via an enum when behavior is two-state.
enum FullGridClearBehavior { ClearToTemplate, ScrollIntoScrollback }
```
