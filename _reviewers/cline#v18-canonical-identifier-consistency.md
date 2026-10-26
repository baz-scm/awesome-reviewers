---
title: Canonical identifier consistency
description: 'When defining or using named identifiers (commands, menu paths, UI assets/icons),
  always rely on the system’s canonical form: apply the same normalization rules everywhere
  and use the shared/canonical source for named assets.'
repository: cline/cline#v18
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70884
---

When defining or using named identifiers (commands, menu paths, UI assets/icons), always rely on the system’s canonical form: apply the same normalization rules everywhere and use the shared/canonical source for named assets.

**Do**
- Normalize named strings at all relevant boundaries (e.g., registration/inspection/execution) using the same canonical rules.
- Prefer canonical/shared imports or component definitions for named UI assets (e.g., icons) so reviewers can confirm consistency by reading code.
- Keep validation aligned with the actual execution model; don’t add “extra” naming rules in one layer if other layers don’t enforce them.

**Don’t**
- Introduce ad-hoc variants (different trimming/spacing rules, different inline icon SVGs) that make it hard to verify which canonical identifier/asset is being used.

**Example (normalization):**
```ts
function normalizeMenuPath(path: string) {
  return path.trim(); // match runner normalization
}

// Use normalizeMenuPath consistently when producing/consuming menu paths
const menuPath = normalizeMenuPath(pluginMenuPath);
``` 

**Example (canonical asset):**
- Instead of embedding a custom inline SVG for an icon in one package, import the same named icon component from the shared library (e.g., Lucide) so the code clearly indicates which icon is used everywhere.