---
title: avoid unnecessary component complexity
description: When designing React components and their APIs, resist the temptation
  to add features, props, or methods that provide limited or no real value to developers.
  Components should expose only functionality that serves genuine use cases and avoids
  introducing maintenance burden or developer confusion.
repository: facebook/react-native
label: React
language: Kotlin
comments_count: 2
repository_stars: 123178
---

When designing React components and their APIs, resist the temptation to add features, props, or methods that provide limited or no real value to developers. Components should expose only functionality that serves genuine use cases and avoids introducing maintenance burden or developer confusion.

Consider whether new props or features will actually be useful in practice. For example, adding a `backgroundColor` prop to a navigation component might seem comprehensive, but if it has no effect with modern gesture navigation, it creates false expectations and API bloat.

Before adding new component features, evaluate:
- Will this prop/feature work consistently across different environments?
- Does it solve a real problem developers face?
- Will it require deprecated APIs or workarounds?
- Does it align with platform conventions and best practices?

Example of what to avoid:
```jsx
// Avoid adding props that don't work consistently
<NavigationBar 
  backgroundColor="#ff0000"  // No effect with gesture navigation
  barStyle="dark"           // Automatic based on contrast
  translucent={true}        // Limited utility
/>
```

Instead, focus on essential functionality that provides clear value:
```jsx
// Focus on props that serve real purposes
<NavigationBar 
  hidden={false}  // Actually controls visibility
/>
```

This principle helps maintain clean, predictable component APIs that developers can rely on without encountering unexpected limitations or deprecated functionality.