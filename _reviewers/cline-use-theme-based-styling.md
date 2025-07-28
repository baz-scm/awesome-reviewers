---
title: Use theme-based styling
description: Always use CSS custom properties (CSS variables) for colors and include
  proper accessibility attributes instead of hard-coded values. This ensures consistency
  with the design system and improves accessibility for users with visual impairments
  or different theme preferences.
repository: cline/cline
label: Code Style
language: TSX
comments_count: 3
repository_stars: 48299
---

Always use CSS custom properties (CSS variables) for colors and include proper accessibility attributes instead of hard-coded values. This ensures consistency with the design system and improves accessibility for users with visual impairments or different theme preferences.

**Color Usage:**
Replace hard-coded color values with theme-based CSS variables:
```tsx
// ❌ Avoid hard-coded colors
style={{
  backgroundColor: "rgba(255, 191, 0, 0.1)",
  border: "1px solid rgba(255, 191, 0, 0.3)",
  color: "#FFA500"
}}

// ✅ Use theme-based colors
style={{
  backgroundColor: "var(--vscode-inputValidation-warningBackground)",
  border: "1px solid var(--vscode-inputValidation-warningBorder)", 
  color: "var(--vscode-inputValidation-warningForeground)"
}}
```

**Accessibility Attributes:**
Include appropriate ARIA labels and roles for interactive elements:
```tsx
// ❌ Missing accessibility attributes
<VSCodeButton onClick={handleCopyCode} title="Copy Code">

// ✅ Include aria-label for screen readers
<VSCodeButton onClick={handleCopyCode} title="Copy Code" aria-label="Copy Code">

// ❌ Clickable div without accessibility
<div onClick={() => { /* handler */ }}>

// ✅ Proper accessibility for interactive elements  
<div onClick={() => { /* handler */ }} aria-label="View HTML Content" role="button" tabIndex={0}>
```

This approach helps users with visual impairments, supports different VS Code themes, and maintains consistency across the application interface.