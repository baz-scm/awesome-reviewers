---
title: Use existing API utilities
description: Always leverage existing utility hooks, constants, and navigation methods
  instead of implementing manual solutions. This ensures consistency across the codebase,
  improves testability, and reduces maintenance overhead.
repository: SigNoz/signoz
label: API
language: TSX
comments_count: 4
repository_stars: 23369
---

Always leverage existing utility hooks, constants, and navigation methods instead of implementing manual solutions. This ensures consistency across the codebase, improves testability, and reduces maintenance overhead.

Key practices:
- Use established hooks like `useUrlQuery` instead of manual URLSearchParams handling
- Define query parameters as constants rather than inline strings
- Use `safeNavigate` instead of `history.replace` for proper browser navigation behavior
- Pass complex state through route state rather than URL parameters for better UX and testability

Example of preferred approach:
```typescript
// Instead of manual URLSearchParams
const { search } = useLocation();
const searchParams = new URLSearchParams(search);

// Use existing utility
const { urlQuery, redirectWithQueryParams } = useUrlQuery();

// Instead of inline strings
searchParams.set('spanId', span.spanId);

// Use constants
searchParams.set(QueryParams.spanId, span.spanId);

// Instead of history.replace
history.replace({ search: searchParams.toString() });

// Use safeNavigate for better UX
safeNavigate({ spanId: span.spanId });
```

This approach promotes code reusability, ensures consistent behavior across components, and makes the codebase more maintainable by centralizing common API interaction patterns.