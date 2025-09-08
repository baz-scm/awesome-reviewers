---
title: prefer simpler patterns
description: Choose simpler, more readable code patterns over complex alternatives
  to improve maintainability and reduce cognitive load. This includes avoiding unnecessary
  complexity in variable assignment, function parameters, and styling approaches.
repository: gravitational/teleport
label: Code Style
language: TSX
comments_count: 4
repository_stars: 19109
---

Choose simpler, more readable code patterns over complex alternatives to improve maintainability and reduce cognitive load. This includes avoiding unnecessary complexity in variable assignment, function parameters, and styling approaches.

Key practices:
- Use destructuring with default values instead of conditional assignment
- Prefer simple variable assignment over Immediately Invoked Function Expressions (IIFE)
- Use object syntax for breakpoints instead of template literals where supported
- Follow mobile-first responsive design patterns with min-width breakpoints

Examples:

Instead of IIFE for complex logic:
```tsx
const hasAccess = (() => {
  if (spec.kind === IntegrationKind.ExternalAuditStorage) {
    return hasIntegrationAccess && hasExternalAuditStorage && enabled;
  }
  return hasIntegrationAccess;
})();
```

Use simple assignment:
```tsx
let hasAccess = hasIntegrationAccess;
if (spec.kind === IntegrationKind.ExternalAuditStorage) {
  hasAccess &&= hasExternalAuditStorage && enabled;
}
```

Instead of conditional assignment:
```tsx
let primaryButtonText = 'Browse Existing Resources';
if (props.primaryButtonText) {
  primaryButtonText = props.primaryButtonText;
}
```

Use destructuring defaults:
```tsx
export function Finished({
  primaryButtonText = 'Browse Existing Resources',
  ...props
}: Props) {
```

This approach reduces indentation, eliminates unnecessary complexity, and makes code intent clearer at first glance.