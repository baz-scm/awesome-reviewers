---
title: Component-agnostic styling principles
description: Create reusable components with styles that don't make assumptions about
  parent contexts or affect their positioning in different applications. Keep positioning
  styles (like margins) in the parent components that use them rather than in the
  reusable component itself. Prefer properties that don't assume parent styling context.
repository: kubeflow/kubeflow
label: Code Style
language: Css
comments_count: 2
repository_stars: 15064
---

Create reusable components with styles that don't make assumptions about parent contexts or affect their positioning in different applications. Keep positioning styles (like margins) in the parent components that use them rather than in the reusable component itself. Prefer properties that don't assume parent styling context.

**Instead of this:**
```scss
// In a reusable component
.panel-body {
  margin-top: 5px;  // Affects positioning
  flex: 1;  // Assumes parent has display: flex
}
```

**Do this:**
```scss
// In a reusable component
.panel-body {
  padding: 1px;  // Internal spacing only
  height: 100%;  // Fills available space without assumptions
}

// In the parent component that uses it
.parent-container .panel-body {
  margin-top: 5px;  // Position-affecting styles belong here
}
```

This approach ensures components remain flexible and can be reused in different contexts without layout issues.
