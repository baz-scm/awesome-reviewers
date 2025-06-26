---
title: "Dry configuration patterns"
description: "Apply DRY (Don't Repeat Yourself) principles to all configuration files to improve maintainability. Extract shared configuration options into reusable constants, especially for values used across multiple environments or settings."
repository: "facebook/react"
label: "Configurations"
language: "JavaScript"
comments_count: 2
repository_stars: 237000
---

Apply DRY (Don't Repeat Yourself) principles to all configuration files to improve maintainability. Extract shared configuration options into reusable constants, especially for values used across multiple environments or settings. This pattern reduces errors when configurations need updating and makes your codebase more maintainable.

For example, instead of duplicating the same rule definitions across different configuration variants:

```js
// Instead of repeated configuration:
export const configs = {
  recommended: {
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
    },
  },
  'flat/recommended': {
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
    },
  }
};

// Extract common configuration to constants:
const sharedRules = {
  'react-hooks/rules-of-hooks': 'error',
  'react-hooks/exhaustive-deps': 'warn',
};

export const configs = {
  recommended: { rules: sharedRules },
  'flat/recommended': { rules: sharedRules }
};
```

This approach also makes it easier to see at a glance which configurations are shared vs. environment-specific, improving code readability and making configuration changes less error-prone.