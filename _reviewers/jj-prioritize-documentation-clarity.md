---
title: prioritize documentation clarity
description: Write documentation that prioritizes user understanding over technical
  precision. Avoid unclear phrases, overly technical explanations, and unhelpful references.
  When in doubt, choose clarity over brevity, especially for user-facing documentation
  that may be someone's first encounter with a feature.
repository: jj-vcs/jj
label: Documentation
language: Rust
comments_count: 7
repository_stars: 21171
---

Write documentation that prioritizes user understanding over technical precision. Avoid unclear phrases, overly technical explanations, and unhelpful references. When in doubt, choose clarity over brevity, especially for user-facing documentation that may be someone's first encounter with a feature.

Key principles:
- Replace unclear phrases with specific, concrete language (e.g., "does not undo the effects on the remote" instead of "does not undo the push itself")
- Add user-friendly explanations for commands and features, explaining their use-case and context
- Simplify overly technical descriptions that sound like code explanations rather than user guidance
- Make references to familiar concepts rather than asking users to "read the source code" or "experiment"
- When documentation might be someone's first reference point, err on the side of being more comprehensive and clear, even if longer

Example of improvement:
```rust
// Before: Technical and unclear
/// Template which, upon being forced (`extract()`ed), will evaluate its
/// condition and select between a template for the true case and a template
/// for the false case (which will yield nothing if it is [`None`]).

// After: Clear and user-focused  
/// Template which selects output based on a boolean condition.
```

This approach ensures documentation serves its primary purpose: helping users understand and effectively use the code.