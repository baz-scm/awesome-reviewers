---
title: preserve URL integrity
description: When manipulating URLs for API calls, prioritize preserving the original
  URL structure over using convenience APIs that may normalize or modify the URL unexpectedly.
  This is especially important when appending query parameters or handling URL fragments.
repository: mountain-loop/yaak
label: API
language: TypeScript
comments_count: 2
repository_stars: 13008
---

When manipulating URLs for API calls, prioritize preserving the original URL structure over using convenience APIs that may normalize or modify the URL unexpectedly. This is especially important when appending query parameters or handling URL fragments.

Use manual string building approaches when you need to maintain exact URL formatting, as browser APIs like `new URL()` may normalize paths, convert case, or modify other URL components in ways that could break existing API integrations.

Example approach for parameter appending:
```typescript
// Avoid: May normalize the URL
const urlObj = new URL(finalUrl);
urlParams.forEach(p => urlObj.searchParams.append(p.name, p.value));

// Prefer: Preserves original URL structure
const [base, hash] = finalUrl.split('#');
const separator = base.includes('?') ? '&' : '?';
const queryString = urlParams
  .map(p => `${encodeURIComponent(p.name)}=${encodeURIComponent(p.value)}`)
  .join('&');
finalUrl = base + separator + queryString + (hash ? `#${hash}` : '');
```

Always test URL manipulation with edge cases including fragments, special characters, and non-standard but valid URL formats to ensure your API calls work with diverse endpoint structures.