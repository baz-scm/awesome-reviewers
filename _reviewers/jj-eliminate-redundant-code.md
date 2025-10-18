---
title: eliminate redundant code
description: Remove unnecessary code, operations, and annotations that don't add value.
  This includes redundant type annotations when types are already constrained, unnecessary
  conditional checks, redundant operations like path normalization in multiple places,
  and overly complex patterns that can be simplified.
repository: jj-vcs/jj
label: Code Style
language: Rust
comments_count: 9
repository_stars: 21171
---

Remove unnecessary code, operations, and annotations that don't add value. This includes redundant type annotations when types are already constrained, unnecessary conditional checks, redundant operations like path normalization in multiple places, and overly complex patterns that can be simplified.

Examples of improvements:
- Remove redundant type annotations: `let out_property: BoxedTemplateProperty<'a, bool> =` → `let out_property =` when the type is already constrained by the function signature
- Simplify conditional logic: `if created_dirs.write().await.insert(dir_path.clone()) {` → just use `created_dirs.write().await.insert(dir_path.clone());` when the condition isn't needed
- Use direct returns: `match expression.evaluate(repo) { Ok(_) => Ok(()), Err(e) => Err(e) }` → `expression.evaluate(repo).map(|_| ())`
- Avoid unnecessary variable assignments: Instead of `let mut hint = ui.hint_default(); writeln!(hint, "...")?;`, directly use `writeln!(ui.hint_default(), "...")?;`
- Remove redundant operations: Don't perform the same normalization (like path canonicalization) in multiple places when it can be done once by the caller

Focus on the principle that code should be as simple and direct as possible while maintaining clarity and correctness.