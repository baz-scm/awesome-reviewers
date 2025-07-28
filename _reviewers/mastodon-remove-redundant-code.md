---
title: remove redundant code
description: Identify and remove code elements that no longer serve a purpose, including
  unused imports, redundant function calls, and obsolete ESLint disable directives.
  This improves code readability and maintainability by eliminating unnecessary clutter.
repository: mastodon/mastodon
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 48691
---

Identify and remove code elements that no longer serve a purpose, including unused imports, redundant function calls, and obsolete ESLint disable directives. This improves code readability and maintainability by eliminating unnecessary clutter.

When refactoring or updating configurations, review the codebase for:
- Imports that are no longer used after removing function calls
- Function calls that duplicate functionality already handled elsewhere (e.g., in application layouts)
- ESLint disable directives that are no longer needed due to rule changes

Example of cleanup:
```typescript
// Before - redundant code
import { start } from 'mastodon/common';
import { loadLocale } from 'mastodon/locales';

// eslint-disable-next-line import/no-default-export
start();

// After - cleaned up
import { loadLocale } from 'mastodon/locales';
```

Regularly audit your code during reviews to ensure only necessary code remains, especially after configuration changes or architectural updates.