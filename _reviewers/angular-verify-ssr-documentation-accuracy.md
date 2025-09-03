---
title: Verify SSR documentation accuracy
description: Ensure that documentation about server-side rendering (SSR), static site
  generation (SSG), and related rendering strategies is technically accurate and complete.
  Avoid making misleading claims about performance characteristics or technical behavior,
  and include all relevant benefits and use cases.
repository: angular/angular
label: Next
language: Markdown
comments_count: 3
repository_stars: 98611
---

Ensure that documentation about server-side rendering (SSR), static site generation (SSG), and related rendering strategies is technically accurate and complete. Avoid making misleading claims about performance characteristics or technical behavior, and include all relevant benefits and use cases.

Common issues to watch for:
- Inaccurate claims about how rendering strategies affect bundle size (bundle size is primarily affected by lazy loading, not rendering strategy)
- Imprecise descriptions of when SSR occurs (e.g., "each request" vs "initial request")
- Missing important benefits like SSR's role in data pre-fetching and server-side data availability

Example of problematic content:
```markdown
## Performance considerations
### Bundle size optimization
Different strategies affect bundle size:
- **SSR**: Initial bundle can be smaller with code splitting
- **SSG**: Optimal with incremental hydration and `@defer`
```

This section makes unsupported claims about SSR/SSG affecting bundle size when the actual factor is lazy loading and code splitting techniques that are independent of rendering strategy.

When documenting rendering strategies, verify technical claims against actual framework behavior and ensure comprehensive coverage of all benefits and limitations.