---
title: eliminate code duplication
description: Actively identify and eliminate code duplication in all its forms to
  improve maintainability and reduce bugs. This includes removing redundant conditional
  checks, extracting common functionality into reusable functions, and avoiding component
  or logic duplication.
repository: PostHog/posthog
label: Code Style
language: TSX
comments_count: 5
repository_stars: 28460
---

Actively identify and eliminate code duplication in all its forms to improve maintainability and reduce bugs. This includes removing redundant conditional checks, extracting common functionality into reusable functions, and avoiding component or logic duplication.

Common patterns to watch for:
- **Redundant conditionals**: Remove duplicate checks that are already handled by parent conditions
- **Duplicated logic blocks**: Extract identical code (except for small variations like keys) into shared functions
- **Component duplication**: Move or reuse existing components instead of creating duplicates
- **Logic reuse**: Leverage existing logic instances rather than reimplementing the same functionality

Example of redundant conditional elimination:
```tsx
// Before: redundant check
{!singleFilter && (
    <div className="ActionFilter-footer">
        {!singleFilter && (  // ❌ Already checked above
            <SomeComponent />
        )}
    </div>
)}

// After: clean structure
{!singleFilter && (
    <div className="ActionFilter-footer">
        <SomeComponent />  // ✅ No redundant check
    </div>
)}
```

Example of extracting duplicated logic:
```tsx
// Before: duplicated except for dismissKey
const billingPeriodEnd = values.billing?.billing_period?.current_period_end?.format('YYYY-MM-DD')
// ... identical logic with different dismissKey

// After: extract to function
const handleDismissal = (dismissKey: string) => {
    const billingPeriodEnd = values.billing?.billing_period?.current_period_end?.format('YYYY-MM-DD')
    // ... shared logic
}
```

Always prefer reusing existing implementations over creating new ones, and extract common patterns into shared utilities when the same logic appears multiple times.