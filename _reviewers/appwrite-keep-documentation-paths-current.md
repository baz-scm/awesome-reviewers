---
title: Keep documentation paths current
description: Maintain accurate and consistent documentation paths, references, and
  descriptions across the codebase. When terminology or architecture changes, ensure
  all documentation references are updated to reflect the current state.
repository: appwrite/appwrite
label: Documentation
language: PHP
comments_count: 7
repository_stars: 51959
---

Maintain accurate and consistent documentation paths, references, and descriptions across the codebase. When terminology or architecture changes, ensure all documentation references are updated to reflect the current state.

Example of proper documentation path updates:
```diff
// In SDK method definition
-description: '/docs/references/databases/update-attribute-enum.md',
+description: '/docs/references/databases/update-column-enum.md',

// In parameter description
-->param('attribute', '', new Key(), 'Document ID.')
+->param('attribute', '', new Key(), 'Attribute key.')
```

Key points:
- Update documentation paths when endpoints or features are renamed
- Ensure parameter descriptions accurately reflect their purpose
- Maintain consistency between code terminology and documentation
- Review all related files when making terminology changes
- Keep API references synchronized with implementation changes