---
title: Follow established naming conventions
description: Ensure all identifiers follow the established naming conventions for
  the codebase and framework being used. This includes using native JavaScript private
  method syntax with `#` instead of underscore prefixes, following camelCase for JavaScript
  methods and variables, matching existing naming patterns for consistency, and avoiding
  deprecated naming...
repository: discourse/discourse
label: Naming Conventions
language: Other
comments_count: 7
repository_stars: 44898
---

Ensure all identifiers follow the established naming conventions for the codebase and framework being used. This includes using native JavaScript private method syntax with `#` instead of underscore prefixes, following camelCase for JavaScript methods and variables, matching existing naming patterns for consistency, and avoiding deprecated naming conventions.

Key guidelines:
- Use native private methods (`#methodName`) instead of underscore prefixes (`_methodName`)
- Follow camelCase for JavaScript identifiers (`copyToClipboard` not `copy_to_clipboard`)
- Match existing naming patterns in the codebase (e.g., plugin outlets should start with `post-`, translation components should use `@key` to match other i18n code)
- Avoid deprecated method names (use `find()` instead of `findBy()`)
- Choose descriptive names that make code self-documenting (`clearSelection()` is clearer than inline `-1`)

Example of preferred private method syntax:
```javascript
// ❌ Avoid underscore prefix
_buildGroupedEvents(detail) {
  // implementation
}

// ✅ Use native private syntax
#buildGroupedEvents(detail) {
  // implementation
}
```

Consistent naming reduces cognitive load, improves code maintainability, and ensures compatibility with modern JavaScript standards and framework conventions.