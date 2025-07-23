---
title: Internationalize all text
description: All user-facing text must be wrapped with translation functions instead
  of using hardcoded English strings. This includes regular UI text, accessibility
  attributes (aria-label, title, alt), and screen reader announcements. Using translation
  keys creates a consistent, maintainable internationalization system and ensures
  the application is accessible to users...
repository: RooCodeInc/Roo-Code
label: Documentation
language: TSX
comments_count: 14
repository_stars: 17288
---

All user-facing text must be wrapped with translation functions instead of using hardcoded English strings. This includes regular UI text, accessibility attributes (aria-label, title, alt), and screen reader announcements. Using translation keys creates a consistent, maintainable internationalization system and ensures the application is accessible to users in all supported languages.

When using translation functions:
- Avoid inline fallback strings in translation calls
- Use structured keys that follow the established naming convention
- Include all necessary context for accurate translation

```typescript
// Incorrect
<h2 className="text-lg font-bold">Something went wrong</h2>
<button title="Add reaction" aria-label="Collapse command management section">
  {screenReaderAnnouncement}
</button>

// Correct
<h2 className="text-lg font-bold">{t("errorBoundary.title")}</h2>
<button 
  title={t("emojiReactions.add")} 
  aria-label={t("chat:commandExecution.collapseManagement")}>
  {t("chat:screenReader.announcement")}
</button>
```

For string interpolation, use translation parameters rather than concatenating strings:

```typescript
// Incorrect
<span>{`File: ${selectedOption.value}, ${selectedMenuIndex + 1} of ${options.length}`}</span>

// Correct
<span>
  {t("chat:contextMenu.announceFile", { 
    name: selectedOption.value, 
    position: t("chat:contextMenu.position", { 
      current: selectedMenuIndex + 1, 
      total: options.length 
    })
  })}
</span>
```