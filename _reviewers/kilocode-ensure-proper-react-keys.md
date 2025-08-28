---
title: Ensure proper React keys
description: Always provide meaningful keys for React components and fragments to
  ensure proper rendering and re-rendering behavior. Use composite keys when component
  identity depends on multiple values, and include keys even for Fragment components
  when rendering lists.
repository: kilo-org/kilocode
label: React
language: TSX
comments_count: 2
repository_stars: 7302
---

Always provide meaningful keys for React components and fragments to ensure proper rendering and re-rendering behavior. Use composite keys when component identity depends on multiple values, and include keys even for Fragment components when rendering lists.

For components that need to re-render based on multiple state changes, create composite keys:
```jsx
<MarketplaceInstallModal
    key={`install-modal-${item.id}-${installModalVersion}`}
    // other props
/>
```

For Fragment components in lists, always include a key prop:
```jsx
{PROVIDERS.map(({ value, label }, i) => (
    <Fragment key={value}>
        <SelectItem value={value}>
            {label}
        </SelectItem>
    </Fragment>
))}
```

This prevents React from incorrectly reusing components and ensures predictable rendering behavior, especially when component state or props change frequently.