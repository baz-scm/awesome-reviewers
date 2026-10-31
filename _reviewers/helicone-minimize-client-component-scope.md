---
title: Minimize client component scope
description: Default to server components and only add `"use client"` to the smallest
  possible component that truly needs it (state, effects, event handlers, or browser
  APIs). Do not mark a parent/page as client just because a nested component is client-side
  - Next.js already interleaves server and client components, and adding the directive
  higher up unnecessarily...
repository: Helicone/helicone
label: Next
language: TSX
comments_count: 2
repository_stars: 6248
---

Default to server components and only add `"use client"` to the smallest possible component that truly needs it (state, effects, event handlers, or browser APIs). Do not mark a parent/page as client just because a nested component is client-side - Next.js already interleaves server and client components, and adding the directive higher up unnecessarily pulls everything underneath into the client bundle. Before adding `"use client"`, ask whether the interactive piece can be isolated into its own small leaf component, and whether the UX benefit justifies the bundle-size/performance cost. For example, if only a hover animation requires client-side state, prefer extracting just that interaction into an isolated client component (or dropping it) rather than converting the whole page/component:

```tsx
// Avoid: marking the whole page client just for a small hover effect
"use client";
export default function CaseStudiesCTA() {
  const [isHovered, setIsHovered] = useState(false);
  // ...
}

// Prefer: keep the page server-rendered; isolate interactivity if truly needed,
// or simplify to avoid client-side state altogether when the benefit is marginal.
export default function CaseStudiesCTA() {
  // server-rendered markup, no client JS shipped
}
```
This keeps client bundles lean and preserves the performance benefits of server rendering.