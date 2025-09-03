---
title: Standardize deprecation documentation
description: When marking APIs, components, or features as deprecated, use consistent
  JSDoc @deprecated tags with clear alternative guidance. This ensures smooth migration
  paths for users and maintains backward compatibility during version transitions.
repository: ant-design/ant-design
label: Documentation
language: TSX
comments_count: 3
repository_stars: 95882
---

When marking APIs, components, or features as deprecated, use consistent JSDoc @deprecated tags with clear alternative guidance. This ensures smooth migration paths for users and maintains backward compatibility during version transitions.

Follow this format:
```typescript
/** @deprecated [ComponentName] is deprecated, please use [AlternativeName] instead */
```

Key principles:
- Always provide a specific alternative or migration path
- Use proper JSDoc syntax for tooling compatibility
- Include the deprecated item name and recommended replacement
- Consider the deprecation timeline - items should remain functional with warnings before removal
- Document the deprecation in a way that guides users toward the preferred solution

Example:
```typescript
/** @deprecated Please use `iconPlacement` instead */
icon?: React.ReactNode;

/** @deprecated DropdownButton is deprecated, please use Space.Compact + Dropdown + Button instead */
```

This approach helps maintain library stability while guiding users toward modern APIs and prevents breaking changes from surprising developers during upgrades.