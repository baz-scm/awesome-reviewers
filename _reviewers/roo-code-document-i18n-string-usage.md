---
title: Document i18n string usage
description: All user-facing strings must be documented with translation function
  usage to ensure proper internationalization support. This includes error messages,
  notifications, labels, and any text displayed to users.
repository: RooCodeInc/Roo-Code
label: Documentation
language: TypeScript
comments_count: 7
repository_stars: 17288
---

All user-facing strings must be documented with translation function usage to ensure proper internationalization support. This includes error messages, notifications, labels, and any text displayed to users.

Example:
```typescript
// ❌ Don't use hardcoded user-facing strings
const notice = `Image file is too large (${imageSizeInMB} MB). The maximum allowed size is 5 MB.`

// ✅ Document translation key usage for user-facing strings
const notice = t('tools:readFile.imageTooLarge', { 
  size: imageSizeInMB,
  max: 5 
})
```

Key requirements:
- Use translation keys in a hierarchical format (e.g., 'category:subcategory.messageId')
- Document parameter interpolation when variables are used
- Include translation key usage in code comments and documentation
- Mark strings as user-facing in documentation when applicable

This ensures maintainable internationalization support and clear documentation of translatable content throughout the codebase.