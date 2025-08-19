---
title: Maintain naming consistency
description: Ensure consistent naming conventions, terminology, and identifiers across
  the entire codebase. Names should be uniform between frontend/backend, across different
  modules, and within the same domain.
repository: PostHog/posthog
label: Naming Conventions
language: TSX
comments_count: 5
repository_stars: 28460
---

Ensure consistent naming conventions, terminology, and identifiers across the entire codebase. Names should be uniform between frontend/backend, across different modules, and within the same domain.

Key areas to check:
- **Cross-system consistency**: Frontend and backend should use the same identifiers for the same concepts (e.g., `search_docs` vs `search_documentation`)
- **Module consistency**: Related modules should use consistent naming patterns (e.g., `sdks` vs `onboarding` logic should align with their actual scope)
- **Terminology consistency**: Use the same terms throughout the codebase for the same concepts (e.g., standardize on "identify respondents" rather than mixing "track/collect/identify responses")
- **Type consistency**: Use the same enums/types across frontend and backend for shared concepts
- **Import consistency**: Consistently use the same import sources (e.g., always use `urls` rather than mixing `urls` and `productUrls`)

Example of inconsistent naming:
```typescript
// Frontend uses different identifier than backend
identifier: 'search_docs' as const,  // Frontend
// vs
search_documentation  // Backend API path

// Mixed terminology in UI
"Track responses to users"
"Collect user responses" 
"Identify respondents"  // Should standardize on one
```

Before merging, verify that new names align with existing patterns and that any changes maintain consistency across all related files and systems.