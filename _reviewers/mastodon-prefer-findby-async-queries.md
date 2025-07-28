---
title: prefer findBy async queries
description: When testing components that require waiting for elements to appear,
  prefer using findBy* queries over waitFor + getBy* combinations. The findBy* queries
  have built-in waiting functionality that makes tests more readable and reliable.
repository: mastodon/mastodon
label: Testing
language: TSX
comments_count: 2
repository_stars: 48691
---

When testing components that require waiting for elements to appear, prefer using findBy* queries over waitFor + getBy* combinations. The findBy* queries have built-in waiting functionality that makes tests more readable and reliable.

Instead of:
```typescript
await waitFor(() => canvas.getByRole('button'));
await userEvent.click(canvas.getByRole('button'));
```

Use:
```typescript
const button = await canvas.findByRole('button');
await userEvent.click(button);
```

This approach reduces code duplication, improves readability, and leverages the testing library's built-in async waiting mechanisms. While some scenarios may still require waitFor for complex conditions, findBy* should be the default choice for waiting for elements to appear.