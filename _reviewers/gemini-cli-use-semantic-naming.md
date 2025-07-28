---
title: Use semantic naming
description: Choose names that clearly communicate the purpose, behavior, and intent
  of variables, methods, classes, and interfaces. Avoid ambiguous or misleading names
  that require additional context to understand.
repository: google-gemini/gemini-cli
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 65062
---

Choose names that clearly communicate the purpose, behavior, and intent of variables, methods, classes, and interfaces. Avoid ambiguous or misleading names that require additional context to understand.

Names should be self-documenting and accurately reflect what the entity represents or does. Consider the actual behavior and usage patterns when naming, not just the initial implementation.

Examples of improvements:
- `SupportedIDE` → `DetectedIde` (clarifies this represents the current IDE, not all supported ones)
- `ActiveFileSchema` → `openFilesSchema` with `filePath` → `activeFilePath` (better reflects the expanding scope)
- `source` → `kind` (more semantic and extensible for different types)
- `interactive` → `forceInteractive` (clarifies it only affects behavior when `-p` flag is present)
- `is_loop` → `loopDetected` (more targeted and descriptive)

When naming conflicts arise or behavior changes, prioritize semantic accuracy over maintaining existing names. The name should help future developers understand the code without needing to read the implementation.