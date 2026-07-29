---
title: Externalize config copy
description: 'Treat user-facing UI text (help text, labels, descriptions, toggle text)
  as configuration: do not hardcode it in components. Instead, source it from the
  appropriate translation/config namespace using the team’s i18n helpers. Keep only
  upstream/system-provided constants (e.g., IDs, template metadata) as raw values
  when they are not user copy.'
repository: diegosouzapw/OmniRoute
label: Configurations
language: TSX
comments_count: 2
repository_stars: 33162
---

Treat user-facing UI text (help text, labels, descriptions, toggle text) as configuration: do not hardcode it in components. Instead, source it from the appropriate translation/config namespace using the team’s i18n helpers. Keep only upstream/system-provided constants (e.g., IDs, template metadata) as raw values when they are not user copy.

Apply this when adding/modifying UI around configuration features (e.g., API key scopes, access descriptions, combo/catalog descriptions).

Example pattern:

```ts
// en.json (or similar)
{
  "apiManager": {
    "managementAccessDesc": "Allow this API key to manage OmniRoute configuration."
  },
  "combos": {
    "autoCatalogTitle": "Auto-routing catalog",
    "autoCatalogDescription": "Built-in auto/* combos resolved dynamically from connected providers."
  }
}
```

```tsx
import { useTranslations } from "next-intl";

const tApi = useTranslations();
const tCombos = useTranslations("combos");

export function Example() {
  return (
    <p>
      {tApi("apiManager.managementAccessDesc")}
      {/* or {tApi("managementAccessDesc")} if already scoped consistently */}
    </p>
  );
}

export function AutoComboHeader() {
  return (
    <h2>{tCombos("autoCatalogTitle")}</h2>
  );
}
```

Checklist:
- New/edited user-facing strings → add to en.json (or the shared config) under the correct namespace.
- Components → useTranslations/use i18n helper instead of inline literals.
- Only translate user copy; leave upstream-defined constants/IDs/metadata as raw values.