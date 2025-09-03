---
title: eliminate code redundancy
description: Remove duplicate imports, unused legacy code, and repetitive patterns
  to maintain clean, organized codebases. Extract commonly used functionality into
  utilities and avoid code duplication through proper abstractions. Use early returns
  to reduce nesting and improve readability.
repository: menloresearch/jan
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 37620
---

Remove duplicate imports, unused legacy code, and repetitive patterns to maintain clean, organized codebases. Extract commonly used functionality into utilities and avoid code duplication through proper abstractions. Use early returns to reduce nesting and improve readability.

Examples of redundancy to eliminate:
- Duplicate imports: Remove repeated import statements like `import { basename } from '@tauri-apps/api/path'` appearing multiple times
- Legacy code cleanup: Remove unused variables and outdated code patterns that no longer serve a purpose
- Utility extraction: Move system-wide functionality like ID generation (`jan-${(Date.now() / 1000).toFixed(0)}`) into shared utilities
- Early returns: Replace nested conditionals with early returns (`if (condition) return` at the start of functions)
- Code duplication: Consolidate similar functionality into reusable abstractions rather than duplicating logic across multiple locations