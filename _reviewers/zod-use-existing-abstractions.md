---
title: Use Existing Abstractions
description: 'Prefer existing framework/library abstractions for both types and layout
  styling to avoid redundant code and one-off visual tweaks.


  - Types: If the framework exposes a prop type, reuse it instead of introducing a
  duplicate interface.'
repository: colinhacks/zod
label: Code Style
language: TSX
comments_count: 2
repository_stars: 42628
---

Prefer existing framework/library abstractions for both types and layout styling to avoid redundant code and one-off visual tweaks.

- Types: If the framework exposes a prop type, reuse it instead of introducing a duplicate interface.
- Spacing/Layout: Apply spacing at the container/layout level and make breakpoint-specific changes explicit (e.g., mobile-only), rather than removing padding/margins on a deeper inner element.

Example:
```tsx
"use client";

import Image, { type ImageProps } from "next/image";

type SidebarLogoProps = ImageProps; // reuse library type

export function SidebarLogo(props: SidebarLogoProps) {
  return (
    <div className="mb-2 md:mb-0"> {/* spacing controlled at container */}
      <Image {...props} />
    </div>
  );
}
```

Apply this during review by checking: (1) are we duplicating types already provided by the dependency? (2) are spacing changes implemented in a maintainable place (container/layout + explicit responsive behavior) rather than ad hoc on an inner div? 