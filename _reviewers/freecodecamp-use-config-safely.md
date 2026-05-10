---
title: Use Config Safely
description: 'Treat configuration/feature-flag-driven logic as potentially different
  between tests and runtime, and standardize how you branch on it.


  Apply this by:'
repository: freeCodeCamp/freeCodeCamp
label: Configurations
language: TSX
comments_count: 2
repository_stars: 444449
---

Treat configuration/feature-flag-driven logic as potentially different between tests and runtime, and standardize how you branch on it.

Apply this by:
1) Verify config-derived outputs with real environment values
- If you compose strings/URLs from config (e.g., base URL + path), ensure runtime values produce the expected final result.
- Don’t rely solely on tests that stub config differently—run locally with the real `GITHUB_LOCATION`/`env.json` setup and confirm the generated links actually work.

2) Prefer the standard feature-flag mechanism for UI
- When the project provides an abstraction (e.g., `IfFeatureEnabled`), use it for feature-controlled UI rather than mixing ad-hoc boolean wrappers that reduce readability and consistency.

3) Keep conditional UI layout consistent
- When rendering conditionally, ensure spacing/layout remains stable and visually intentional.

Example pattern (feature-controlled UI):
```tsx
<IfFeatureEnabled feature='classroom-mode'>
  <Spacer size='m' />
  <ClassroomMode
    isClassroomAccount={isClassroomAccount}
    updateIsClassroomAccount={updateIsClassroomAccount}
  />
</IfFeatureEnabled>
```