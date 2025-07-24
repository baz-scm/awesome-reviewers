---
title: Clean and consistent code
description: 'Maintain clean and consistent code by removing unnecessary elements
  and following standard practices:


  1. **Remove commented-out code and unused imports** - Don''t leave commented-out
  code in the codebase. If code is no longer needed, delete it entirely rather than
  commenting it out. Similarly, remove unused imports to reduce bundle size and avoid
  linting...'
repository: n8n-io/n8n
label: Code Style
language: Other
comments_count: 12
repository_stars: 122978
---

Maintain clean and consistent code by removing unnecessary elements and following standard practices:

1. **Remove commented-out code and unused imports** - Don't leave commented-out code in the codebase. If code is no longer needed, delete it entirely rather than commenting it out. Similarly, remove unused imports to reduce bundle size and avoid linting errors.

```javascript
// Bad
import { computed, watch } from 'vue'; // watch is never used

// Good
import { computed } from 'vue';

// Bad
// const { getReportingURL } = useBugReporting();
// <LogoText v-if="showLogoText" :class="$style.logoText" />

// Good
// Import only what's needed, remove completely when no longer used
```

2. **Follow CSS best practices** - Use standard CSS properties and valid values. Avoid non-standard attributes and properties that may not work across all browsers.

```css
/* Bad */
.container {
  justify-content: right; /* Invalid value */
}
<style v-if="content.css" type="text/css" scoped> /* Non-standard usage */

/* Good */
.container {
  justify-content: flex-end; /* Standard value */
}
```

3. **Avoid dead code** - Remove CSS selectors that don't correspond to elements in your templates, and delete unused functions and variables.

```css
/* Bad - selector with no matching elements */
.titleInput input {
  /* styles that will never be applied */
}
```

4. **Don't disable lint rules inline** - Instead of disabling lint rules with inline comments, fix the underlying issue or configure the rule project-wide if necessary.

```javascript
// Bad
// eslint-disable-next-line @typescript-eslint/return-await
return await somePromise();

// Good
return somePromise(); // Fix the underlying issue instead
```

Following these practices improves code readability, reduces maintenance overhead, and prevents subtle bugs from entering your codebase.