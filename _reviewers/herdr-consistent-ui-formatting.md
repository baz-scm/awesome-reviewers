---
title: Consistent UI formatting
description: When formatting UI text for alignment (padding/truncation like `{position:<N}`),
  keep the visual rules consistent across all related components and validate against
  the actual available width. If the change would alter the product’s visual language/layout
  rules (e.g., needing new rules to display a dot for 100+), treat it as a design/discussion
  item rather...
repository: ogulcancelik/herdr
label: Code Style
language: Rust
comments_count: 2
repository_stars: 26924
---

When formatting UI text for alignment (padding/truncation like `{position:<N}`), keep the visual rules consistent across all related components and validate against the actual available width. If the change would alter the product’s visual language/layout rules (e.g., needing new rules to display a dot for 100+), treat it as a design/discussion item rather than bundling it into a narrowly scoped fix.

How to apply:
- Follow the existing convention used by the neighboring UI (if one list uses `{position:<2}`, other lists that render the same “position” should use the same convention).
- Check layout constraints first (e.g., available columns in the target area); don’t assume the padding will “fit” for larger values.
- Scope correctly: keep “fix” PRs within the agreed display range; move visual-language/width-rule changes to a separate discussion.

Example (consistent padding):
```rust
// Keep the same position formatting convention used by other lists.
Span::styled(format!("{:<2}", visible_idx + 1), num_style)
```