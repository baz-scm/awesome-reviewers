---
title: Explicit configuration resolution
description: Always use explicit path resolution and document ordering requirements
  in configuration files to prevent environment-dependent issues. This makes configurations
  more reliable and self-documenting.
repository: mui/material-ui
label: Configurations
language: JavaScript
comments_count: 3
repository_stars: 96063
---

Always use explicit path resolution and document ordering requirements in configuration files to prevent environment-dependent issues. This makes configurations more reliable and self-documenting.

For file paths in configuration files:
- Use `require.resolve()` instead of relative paths to ensure consistent resolution across environments
- Document plugin or dependency ordering requirements with clear comments
- Include references to official documentation when specific ordering is required

**Example:**

```javascript
// Bad
module.exports = {
  extends: [
    'eslint-config-airbnb',
    './eslint/config-airbnb-typescript.js',
  ]
};

// Good
module.exports = {
  extends: [
    'eslint-config-airbnb',
    require.resolve('./eslint/config-airbnb-typescript.js'),
  ]
};

// Even better - with documentation
const plugins = [];

// must be loaded last: https://github.com/tailwindlabs/prettier-plugin-tailwindcss?tab=readme-ov-file#compatibility-with-other-prettier-plugins
plugins.push('prettier-plugin-tailwindcss');

// For complex environment variables, include thorough documentation
/**
 * Fun facts about the `process.env.CONTEXT`:
 * - It is defined by Netlify environment variables
 * - `process.env.CONTEXT === 'production'` means...
 */
```

This approach prevents subtle configuration bugs that only appear in certain environments, reduces onboarding friction for new developers, and creates self-documenting configuration files.