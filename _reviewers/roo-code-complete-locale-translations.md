---
title: Complete locale translations
description: Ensure that all text strings in locale-specific files are properly translated
  into their respective languages. Leaving untranslated English text in non-English
  locale files creates an inconsistent user experience and reduces the effectiveness
  of localization efforts.
repository: RooCodeInc/Roo-Code
label: Documentation
language: Json
comments_count: 25
repository_stars: 17288
---

Ensure that all text strings in locale-specific files are properly translated into their respective languages. Leaving untranslated English text in non-English locale files creates an inconsistent user experience and reduces the effectiveness of localization efforts.

When adding new features or UI elements:
1. Identify all strings that need translation
2. Ensure translations are provided for every supported language
3. Verify that no English text remains in non-English locale files
4. Use native punctuation conventions of the target language

Example of a problem:
```json
// webview-ui/src/i18n/locales/es/mcp.json
{
  "serverStatus": {
    "retrying": "Reintentando...",
    "retryConnection": "Reintentar conexión",
    "disabled": "Server is disabled"  // English text in Spanish file
  }
}
```

Correct implementation:
```json
// webview-ui/src/i18n/locales/es/mcp.json
{
  "serverStatus": {
    "retrying": "Reintentando...",
    "retryConnection": "Reintentar conexión",
    "disabled": "Servidor deshabilitado"  // Properly translated to Spanish
  }
}
```