---
title: Simplify feature flag logic
description: 'When working with feature flags and configuration conditions, keep your
  logic clean and up-to-date:


  1. **Simplify conditionals when flag states change**: When a feature flag becomes
  permanently enabled or disabled, update and simplify all conditionals that reference
  it.'
repository: getsentry/sentry
label: Configurations
language: TSX
comments_count: 3
repository_stars: 41297
---

When working with feature flags and configuration conditions, keep your logic clean and up-to-date:

1. **Simplify conditionals when flag states change**: When a feature flag becomes permanently enabled or disabled, update and simplify all conditionals that reference it.

2. **Access feature flags directly**: Prefer checking feature flags directly rather than through abstraction layers that may become deprecated.

3. **Track feature state changes accurately**: When determining if a feature was newly activated, compare current state with previous state rather than relying only on current selections.

Example refactoring when a feature flag is now always true:
```typescript
// Before: Complex condition with useEap feature flag
enabled: Boolean(webVital) && (useEap || isInp || (isSpansWebVital && useSpansWebVitals))

// After: Simplified condition since useEap is always true
enabled: Boolean(webVital) && (isInp || (isSpansWebVital && useSpansWebVitals))
```

Example for checking feature flags directly:
```typescript
// Avoid using abstraction components for feature checking
<Feature features="organizations:user-feedback-ai-summaries">
  {/* Component content */}
</Feature>

// Prefer direct access to feature flags
{organization.features.includes('organizations:user-feedback-ai-summaries') && (
  /* Component content */
)}
```