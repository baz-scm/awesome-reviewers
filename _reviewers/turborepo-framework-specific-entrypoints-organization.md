---
title: Framework-specific entrypoints organization
description: When creating libraries that integrate with Next.js or other frameworks,
  organize your code with separate entrypoints for each supported framework. This
  approach improves bundling efficiency, prevents dependency conflicts, and makes
  framework-specific code easier to maintain.
repository: vercel/turborepo
label: Next
language: Other
comments_count: 2
repository_stars: 28115
---

When creating libraries that integrate with Next.js or other frameworks, organize your code with separate entrypoints for each supported framework. This approach improves bundling efficiency, prevents dependency conflicts, and makes framework-specific code easier to maintain.

Structure your exports with clear path separation:
- Use a base path for framework-agnostic components
- Use framework-specific paths for specialized integrations

For example:

```js
// In your package.json exports
{
  "exports": {
    "./link": "./dist/link.js",         // Basic HTML component
    "./next-js/link": "./dist/next-link.js",  // Next.js specific implementation
    "./svelte/link": "./dist/svelte-link.js"  // Svelte specific implementation
  },
  "peerDependencies": {
    "next": ">=15"  // Specify version ranges when possible
  }
}
```

In your framework-specific implementation:

```tsx
// ./packages/ui/src/next-link.tsx
import Link from 'next/link';
import type { ComponentProps } from 'react';

type CustomLinkProps = ComponentProps<typeof Link>;

export function CustomLink({ children, ...props }: CustomLinkProps) {
  return (
    <Link className="text-underline hover:text-green-400" {...props}>
      {children}
    </Link>
  );
}
```

This pattern allows consumers to import exactly what they need while bundlers can properly tree-shake unused framework code. It also enhances type safety since framework-specific props and behaviors are isolated to their respective entrypoints.