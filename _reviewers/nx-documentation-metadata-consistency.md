---
title: Documentation metadata consistency
description: Ensure documentation uses consistent structural elements and proper metadata
  to optimize user experience and content discoverability. Use platform-native components
  (like `aside` instead of `callout` for Astro docs), include appropriate sidebar
  labels, and leverage weight/filter properties to control search result prominence.
repository: nrwl/nx
label: Documentation
language: Other
comments_count: 4
repository_stars: 27518
---

Ensure documentation uses consistent structural elements and proper metadata to optimize user experience and content discoverability. Use platform-native components (like `aside` instead of `callout` for Astro docs), include appropriate sidebar labels, and leverage weight/filter properties to control search result prominence.

Key practices:
- Use consistent documentation components that are native to your platform
- Add explicit sidebar labels when the page title isn't suitable for navigation
- Use weight values (like 0.1 or 0.5) to deprioritize less useful content in search results
- Apply filter metadata to categorize content appropriately

Example frontmatter:
```yaml
---
title: 'affected:graph - CLI command'
sidebar:
  label: Introduction
weight: .1
filter: "type:References"
---
```

This approach prevents deprecated or less relevant content from dominating search results while ensuring users can navigate documentation intuitively.