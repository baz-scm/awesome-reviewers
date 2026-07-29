---
title: Localize configuration UI
description: In configuration/settings UI (including timezone, system defaults, and
  messaging), do not introduce or hardcode user-visible text. Always source strings
  from the appropriate i18n catalog/keys so all locales (e.g., desktop Japanese/Chinese)
  get consistent wording.
repository: nousresearch/hermes-agent
label: Configurations
language: TSX
comments_count: 2
repository_stars: 221948
---

In configuration/settings UI (including timezone, system defaults, and messaging), do not introduce or hardcode user-visible text. Always source strings from the appropriate i18n catalog/keys so all locales (e.g., desktop Japanese/Chinese) get consistent wording.

Apply this rule:
- Prefer existing localized keys (e.g., `t.common.messaging`) instead of literals.
- If the UI requires new copy (e.g., “System default” wording, empty state text, truncation/capped-list hints), add/update the string in the desktop/web i18n catalogs and then reference it from code.
- When the same concept is used across platforms, keep the wording consistent by updating the canonical i18n entries.

Example pattern (web):
```ts
// Good: use localized key
const label = t.common.messaging

// Avoid:
const label = 'Messaging' // forces English
```

Example pattern (component string reuse):
```ts
// Good: pull “System default” and related hints from i18n
const systemDefaultText = t.config.systemDefault
```