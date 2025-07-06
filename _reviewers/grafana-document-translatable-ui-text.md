---
title: Document translatable UI text
description: All user-facing text in UI components should be properly documented for
  translation using the application's internationalization (i18n) framework. This
  ensures that the application can be easily localized for different regions and improves
  maintainability.
repository: grafana/grafana
label: Documentation
language: TSX
comments_count: 2
repository_stars: 68825
---

All user-facing text in UI components should be properly documented for translation using the application's internationalization (i18n) framework. This ensures that the application can be easily localized for different regions and improves maintainability.

When adding text to a component:
1. Import the translation utilities: `import { t, Trans } from '@grafana/i18n';`
2. Use the `t` function with specific, namespaced translation keys
3. Always provide the English default text as the second parameter
4. Don't forget to translate accessibility text (aria-labels, titles)

**Example:**
```tsx
// DON'T do this (hardcoded strings):
const openPrText = isFolder
  ? 'A new folder has been created in a pull request in GitHub.'
  : 'This dashboard is loaded from a pull request in GitHub.';

// DO this instead (properly documented for translation):
const openPrText = isFolder
  ? t('provisioned-dashboard-preview-banner.title-folder-created', 'A new folder has been created in a pull request in GitHub.')
  : t('provisioned-dashboard-preview-banner.title-dashboard-loaded', 'This dashboard is loaded from a pull request in GitHub.');

// For button text and other UI elements:
<Button
  icon="angle-left"
  aria-label={t('return-to-previous.aria-label', 'Return to previous page')}
>
  {t('return-to-previous.button-text', 'Back to {destination}', { destination: shortenTitle(children) })}
</Button>
```

Using standardized translation keys with descriptive namespaces improves code documentation and makes it easier for translators to understand the context of each string.