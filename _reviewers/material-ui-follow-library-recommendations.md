---
title: Follow library recommendations
description: When writing tests, prioritize following the official recommendations
  and best practices of testing libraries (like Playwright) even if they appear more
  verbose than alternatives. Library recommendations typically address edge cases,
  improve reliability, and future-proof your tests.
repository: mui/material-ui
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 96063
---

When writing tests, prioritize following the official recommendations and best practices of testing libraries (like Playwright) even if they appear more verbose than alternatives. Library recommendations typically address edge cases, improve reliability, and future-proof your tests.

For example, prefer:
```typescript
// Recommended approach
const errorSelector = page.locator('.MuiInputBase-root.Mui-error');
await errorSelector.waitFor();
```

Instead of:
```typescript
// Discouraged approach
await page.waitForSelector('.MuiInputBase-root.Mui-error');
```

This applies to all testing libraries and frameworks. While deprecated or discouraged methods might sometimes appear cleaner or more straightforward, the recommended approaches usually incorporate lessons learned from the wider community and prevent subtle issues from arising in different environments or future versions.