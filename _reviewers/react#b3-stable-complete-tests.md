---
title: Stable, Complete Tests
description: 'Ensure tests are both comprehensive and deterministic:


  1) Cover invariants across the full output surface (not just a subset) and validate
  them consistently for every backend. When you’re checking source ranges/locations,
  assert the full set of expected relationships (e.g., numeric `start/end` align with
  `loc.*.index`, and ordering constraints like `start...'
repository: facebook/react#b3
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 251883
---

Ensure tests are both comprehensive and deterministic:

1) Cover invariants across the full output surface (not just a subset) and validate them consistently for every backend. When you’re checking source ranges/locations, assert the full set of expected relationships (e.g., numeric `start/end` align with `loc.*.index`, and ordering constraints like `start <= end`), and run the same logic for all backends.

2) For E2E/UI tests, avoid brittle selectors based on DOM position (like `.nth(n)`). Prefer explicit, stable selectors such as `data-testid` and add scenario variants for key toggles (e.g., “internals shown” vs “internals hidden”).

Example (range invariant assertion pattern):
```ts
function assertRanges(node: any) {
  if (!node || typeof node.start !== 'number' || typeof node.end !== 'number') return;
  const locStart = node.loc?.start?.index;
  const locEnd = node.loc?.end?.index;
  const start = node.start;
  const end = node.end;

  if (typeof locStart === 'number') if (start !== locStart) throw new Error('start mismatch');
  if (typeof locEnd === 'number') if (end !== locEnd) throw new Error('end mismatch');
  if (start > end) throw new Error('invalid range ordering');
}
```

Example (deterministic E2E selection):
```ts
// Prefer test ids over positional nth() selectors.
await page.getByTestId('config-tab').locator('.monaco-editor').first().allInnerTexts();
```