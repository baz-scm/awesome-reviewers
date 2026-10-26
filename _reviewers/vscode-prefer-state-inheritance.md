---
title: Prefer state inheritance
description: When styling component states (e.g., selected/active), keep descendant
  visuals consistent by using inheritance and tightly scoped rules—and manage the
  cascade without descendant-state selectors or `!important`.
repository: microsoft/VSCode
label: Code Style
language: Css
comments_count: 2
repository_stars: 194303
---

When styling component states (e.g., selected/active), keep descendant visuals consistent by using inheritance and tightly scoped rules—and manage the cascade without descendant-state selectors or `!important`.

**Do**
- Propagate parent state to children that render stateful text/icons:
  - Use a targeted selected/active descendant rule and let the child inherit from the parent.
- Avoid descendant-state selectors (like `:has()`) for owned UI state. Instead, add a **stable marker class** to the specific DOM node you own, then scope styles with regular selectors.
- Avoid using non-focus `!important` to “fight” framework defaults; prefer scoped specificity (component/root scoping + marker classes).

**Example**
```css
/* Selected state should propagate to the child label */
.ai-customization-management-editor
  .sidebar-migration-button.selected {
  background-color: var(--vscode-list-activeSelectionBackground);
  color: var(--vscode-list-activeSelectionForeground);
}

.ai-customization-management-editor
  .sidebar-migration-button.selected
  .sidebar-migration-count {
  color: inherit;
}

/* Instead of :has(), use a stable marker class and scope specificity */
.ai-customization-management-editor
  .embedded-detail-fact-value--has-actions {
  /* stateful styles here */
}
```

**Rule of thumb:** if the visual state depends on “what descendants exist,” prefer a marker class on the owning node; if the visual state depends on “being selected,” prefer inheritance plus a targeted selected/active descendant selector.