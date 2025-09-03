---
title: Consistent naming patterns
description: Establish and enforce consistent naming conventions across different
  contexts in your codebase. Teams should decide on specific patterns and use linting
  to maintain consistency rather than mixing approaches.
repository: cypress-io/cypress
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 48850
---

Establish and enforce consistent naming conventions across different contexts in your codebase. Teams should decide on specific patterns and use linting to maintain consistency rather than mixing approaches.

Key areas to standardize:

**Props access**: Choose either `props.showBrowsers` or destructured `showBrowsers` consistently throughout the codebase. As noted in discussions: "we should lint for one or the other" rather than mixing both approaches.

**Component naming**: Use PascalCase for custom Vue components (`RouterLink`) and kebab-case for native HTML elements and built-in Vue components (`router-link`). Avoid mixing casing styles within the same context.

**GraphQL fragments**: Adopt a consistent naming pattern like `ComponentName_UniqueName` for all fragments, even when there's only one per component. This prevents naming conflicts and maintains predictability.

Example of inconsistent vs consistent patterns:
```vue
<!-- Inconsistent -->
<template>
  <router-link :to="props.href">  <!-- mixing kebab-case component with props. access -->
    <HeaderContent :show-browsers="showBrowsers" />  <!-- mixing destructured props -->
  </router-link>
</template>

<!-- Consistent -->
<template>
  <RouterLink :to="href">  <!-- PascalCase for custom components -->
    <HeaderContent :show-browsers="showBrowsers" />  <!-- consistent props access -->
  </RouterLink>
</template>
```

The goal is to eliminate decision fatigue and reduce cognitive load by having clear, lintable rules that the entire team follows consistently.