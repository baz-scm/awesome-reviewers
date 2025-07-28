---
title: Strategic component loading
description: Choose component loading strategies based on when interactivity is actually
  needed, not just code splitting. Lazy prefixed components only control chunk size
  but still load eagerly with the page's scripts. Use delayed hydration for components
  that don't need immediate interactivity, avoiding unnecessary JavaScript execution
  during initial page load. Be...
repository: nuxt/nuxt
label: Performance Optimization
language: Markdown
comments_count: 4
repository_stars: 57769
---

Choose component loading strategies based on when interactivity is actually needed, not just code splitting. Lazy prefixed components only control chunk size but still load eagerly with the page's scripts. Use delayed hydration for components that don't need immediate interactivity, avoiding unnecessary JavaScript execution during initial page load. Be cautious with server components and nested islands as they can create request waterfalls and add overhead.

```html
<template>
  <div>
    <!-- ❌ Lazy component still loads eagerly -->
    <LazyMountainsList v-if="show" />
    
    <!-- ✅ Delayed hydration loads component just-in-time -->
    <LazyMyComponent hydrate-on-visible />
    
    <!-- ❌ Avoid nesting islands (creates waterfall) -->
    <ServerComponentA>
      <ServerComponentB /> <!-- Each island adds overhead -->
    </ServerComponentA>
  </div>
</template>
```

Prioritize delayed hydration for below-the-fold components, use lazy components primarily for code organization, and avoid patterns that create request waterfalls or unnecessary overhead during the critical rendering path.