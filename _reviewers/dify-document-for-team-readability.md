---
title: Document for team readability
description: Ensure code includes appropriate documentation to improve readability
  and help team members understand and work with the codebase effectively. This includes
  adding JSDoc comments for new components and features, and preserving existing documentation
  patterns like internationalization keys that serve as format specifications.
repository: langgenius/dify
label: Documentation
language: TSX
comments_count: 2
repository_stars: 114231
---

Ensure code includes appropriate documentation to improve readability and help team members understand and work with the codebase effectively. This includes adding JSDoc comments for new components and features, and preserving existing documentation patterns like internationalization keys that serve as format specifications.

For new components, add JSDoc comments explaining purpose and functionality:

```typescript
/**
 * Audio configuration component that manages file upload settings
 * for audio files in the workflow features
 */
const ConfigAudio: FC = () => {
  // component implementation
}
```

When refactoring, maintain existing documentation patterns rather than removing them:

```typescript
// Keep i18n keys that document expected formats
const timeFormat = needTimePicker ? t('time.dateFormats.displayWithTime') : t('time.dateFormats.display')
// Instead of hardcoded strings like 'YYYY-MM-DD HH:mm'
```

Well-documented code increases readability and makes it easier for other developers to pick up and work with unfamiliar code sections.