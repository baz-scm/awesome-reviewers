---
title: Canonical naming consistency
description: Use a single canonical form for identifiers (including normalization)
  and a single canonical source for named assets, so code paths and reviewers can
  reliably trace what’s being used.
repository: cline/cline#v23
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70889
---

Use a single canonical form for identifiers (including normalization) and a single canonical source for named assets, so code paths and reviewers can reliably trace what’s being used.

Apply this in practice:
- Normalize at the boundary where identifiers are compared/serialized (e.g., paths/command names) using the same normalization rules as the runtime/runner.
- Keep validation/allow-listing behavior consistent across the full lifecycle (registration → inspection → execution). Don’t introduce extra “tolerant” validation in one stage if other stages don’t do it.
- For shared named UI assets (icons/components), import/use the same canonical component/source everywhere so it’s easy to verify identity in code.

Example (identifier normalization):
```ts
// Ensure the menu/command path matches the runner's normalization
const normalizedPath = menuPath.trim();
// Use normalizedPath consistently anywhere the path is inspected/registered/executed
registerCommand(normalizedPath, handler);
```