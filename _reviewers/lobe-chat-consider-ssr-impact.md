---
title: Consider SSR impact
description: When using Next.js dynamic imports, carefully evaluate whether to disable
  server-side rendering (SSR) based on the component's purpose and impact on user
  experience.
repository: lobehub/lobe-chat
label: Next
language: TSX
comments_count: 3
repository_stars: 65138
---

When using Next.js dynamic imports, carefully evaluate whether to disable server-side rendering (SSR) based on the component's purpose and impact on user experience.

**Keep SSR enabled (default) when:**
- Component has layout implications (height, positioning) that could cause layout shifts if missing during initial render
- Component is part of the main content flow

**Disable SSR (`ssr: false`) when:**
- Component handles client-side errors and needs full client control for proper error display
- Component is a modal or overlay that doesn't affect initial page layout
- Component requires browser-only APIs or client-side state

**Example:**
```tsx
// ❌ Avoid for layout-affecting components
const CloudBanner = dynamic(() => import('@/features/AlertBanner/CloudBanner'), { ssr: false });

// ✅ Good for error handling
export default dynamic(() => import('@/components/Error'), { ssr: false });

// ✅ Consider for modals
const ModalContent = dynamic(() => import('./ModalContent'), { ssr: false });
```

The key is preventing layout shifts while ensuring functionality works correctly across SSR and client-side rendering.