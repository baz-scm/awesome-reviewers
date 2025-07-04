---
title: Internationalize ui text
description: All user interface text must be internationalized using the appropriate
  i18n module instead of hardcoded strings. This ensures the application can be properly
  localized for different languages and regions.
repository: apache/airflow
label: Documentation
language: TSX
comments_count: 5
repository_stars: 40858
---

All user interface text must be internationalized using the appropriate i18n module instead of hardcoded strings. This ensures the application can be properly localized for different languages and regions.

Key implementation guidelines:
- Use the `useTranslation` hook to access translation strings
- Store translations in dedicated language files (e.g., `en/common.json`, `en/dashboard.json`)
- Ensure all UI elements are translatable including labels, placeholders, and aria-labels
- Do not use inline comments for translation hints

Example:
```tsx
// Incorrect approach
<Heading ml={1} size="xs">
  Favorite Dags
</Heading>

// Correct approach
import { useTranslation } from "react-i18next";

// Within component
const { t: translate } = useTranslation("dashboard");

<Heading ml={1} size="xs">
  {translate("favorite.favoriteDags")}
</Heading>
```

When adding new UI text:
1. Update the appropriate translation file with a clear, descriptive key
2. Focus on maintaining translations for languages you're familiar with
3. Other languages will fall back to English until translated by appropriate contributors

This practice improves accessibility, enables global adoption, and follows proper documentation standards for international software.