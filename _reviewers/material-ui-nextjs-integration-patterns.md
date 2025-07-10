---
title: Next.js integration patterns
description: When integrating with Next.js, follow framework-specific patterns carefully
  and stay updated with API changes to ensure proper server-side rendering and optimal
  code.
repository: mui/material-ui
label: Next
language: TSX
comments_count: 2
repository_stars: 96063
---

When integrating with Next.js, follow framework-specific patterns carefully and stay updated with API changes to ensure proper server-side rendering and optimal code.

For SSR styling with libraries like Emotion:
- Call initialization functions in the correct sequence
- Document critical side effects that affect rendering

```tsx
// ✅ DO: Call createEmotionServer immediately after cache creation with explanatory comment
const cache = createEmotionCache();
// The createEmotionServer has to be called directly after the cache creation due to the side effect of cache.compat = true,
// otherwise the styles won't be properly placed in the head tag
const { extractCriticalToChunks } = createEmotionServer(cache);

// ❌ DON'T: Call functions without understanding sequence dependencies
const cache = createEmotionCache();
// Other code...
const { extractCriticalToChunks } = createEmotionServer(cache); // Too late, SSR styling will be broken
```

Additionally, regularly review the official Next.js documentation to remove deprecated patterns (like unnecessary `passHref` props in newer versions) and adopt current recommended practices.