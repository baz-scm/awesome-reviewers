---
title: Consistent Test ID Naming
description: 'When adding or modifying UI elements, ensure their test/automation identifiers
  follow the existing naming conventions and remain stable.


  Apply these rules:'
repository: maximhq/bifrost
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 6862
---

When adding or modifying UI elements, ensure their test/automation identifiers follow the existing naming conventions and remain stable.

Apply these rules:
- Prefer component-supported prefixing (e.g., `testIdPrefix`) so generated IDs stay consistent across related CTAs.
- If you must set `data-testid` directly, follow the local established pattern for that area (for example, `client-settings-<name>-<element>` where `<element>` reflects the control type like `switch` / `input`).
- Keep identifiers predictable: use a scope/feature prefix, then the setting/feature name, then the UI element type.

Example patterns:

```tsx
// Prefer prefix props when the component generates IDs
<ContactUsView
  testIdPrefix="license"
  title="Unlock license management"
  // generated IDs like: license-read-more / license-book-demo
/>

// Follow the local convention when setting explicitly
<Switch
  id="dump-errors-in-console-logs"
  data-testid="client-settings-dump-errors-switch"
  // ...
/>
```

This keeps automated tests resilient and avoids one-off/unstable identifiers that break CI and slow down debugging.