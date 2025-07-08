---
title: Prefer server components
description: 'Default to server components in Next.js applications to maximize the
  benefits of server-side rendering. Avoid adding "use client" directives unnecessarily,
  especially at the page level. '
repository: prowler-cloud/prowler
label: Next
language: TSX
comments_count: 2
repository_stars: 11834
---

Default to server components in Next.js applications to maximize the benefits of server-side rendering. Avoid adding "use client" directives unnecessarily, especially at the page level. 

When building features:
1. Start with server components
2. Only add "use client" when you need client-side interactivity
3. Keep "use client" directives as low in the component tree as possible

For configurations or data that doesn't require client-side interactivity, handle them directly in Next.js layouts or server components rather than introducing additional client components.

**Example - Avoid:**
```tsx
// ui/app/(prowler)/lighthouse/config/page.tsx
"use client"; // Unnecessary - prevents server-side rendering
```

**Example - Prefer:**
```tsx
// Keep pages as server components
// Only mark specific interactive components with "use client"
// ui/components/interactive-feature.tsx
"use client"; // Only where needed for client-side functionality
```

This approach leverages Next.js 14's SSR capabilities, improves performance, and aligns with the project's architecture.