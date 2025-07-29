---
title: documentation linking standards
description: Ensure proper linking and cross-referencing in documentation to improve
  navigation and discoverability. Use correct JSDoc syntax for type references and
  consistently link to related concepts where they are mentioned.
repository: remix-run/react-router
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 55270
---

Ensure proper linking and cross-referencing in documentation to improve navigation and discoverability. Use correct JSDoc syntax for type references and consistently link to related concepts where they are mentioned.

For TypeScript types in JSDoc comments, use `{@link TypeName}` syntax instead of markdown-style links:

```tsx
/**
 * The {@link Blocker} object returned by the hook has the following properties:
 */
```

Cross-link to related concepts when they are mentioned in documentation text:

```markdown
These are the requests that return the [`loader`][loader] and [`action`][action] data to the browser.
```

Link hooks and components where they are referenced rather than only in "See" sections:

```markdown
You can use [`<Link state>`][link-component-state-prop] or [`useNavigate`][use-navigate] to change the location state.
```

This practice helps users discover related functionality and creates a more interconnected documentation experience that reduces the need to search for related concepts separately.