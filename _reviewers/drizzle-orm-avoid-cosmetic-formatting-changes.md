---
title: avoid cosmetic formatting changes
description: Avoid including purely cosmetic formatting changes in pull requests that
  serve a functional purpose. Automatic formatter changes (like Prettier reformatting,
  bracket placement, or line breaks) should be separated from functional changes to
  keep PRs focused and easier to review and merge.
repository: drizzle-team/drizzle-orm
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 29461
---

Avoid including purely cosmetic formatting changes in pull requests that serve a functional purpose. Automatic formatter changes (like Prettier reformatting, bracket placement, or line breaks) should be separated from functional changes to keep PRs focused and easier to review and merge.

When submitting PRs, ensure changes contain the "absolute minimum amount of changes compared to the version you are editing" for faster approval. If you need to apply formatting changes, consider doing so in a separate, dedicated formatting-only PR.

Example of cosmetic changes to avoid mixing with functional changes:
```typescript
// Before (functional change mixed with formatting)
-	generated: T extends { generated: infer G } ? G extends undefined ? unknown : G : unknown;
-}
-& TTypeConfig
+	generated: T extends { generated: infer G } ? (G extends undefined ? unknown : G) : unknown;
+} & TTypeConfig

// Better: Keep functional changes separate from formatting changes
```

This practice improves code review efficiency and reduces the likelihood of merge conflicts.