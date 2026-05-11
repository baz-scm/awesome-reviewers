---
title: Maintain Predictable Configs
description: 'Configuration files should be predictable for every developer and remain
  maintainable over time.


  - Prefer explicit, stable values in runtime/version files (pin a specific version)
  so `nvm use`/install instructions work consistently. If you use an alias (like an
  LTS channel), ensure the exact alias form is supported (e.g., correct casing) and
  document why...'
repository: tanstack/query
label: Configurations
language: Other
comments_count: 2
repository_stars: 49380
---

Configuration files should be predictable for every developer and remain maintainable over time.

- Prefer explicit, stable values in runtime/version files (pin a specific version) so `nvm use`/install instructions work consistently. If you use an alias (like an LTS channel), ensure the exact alias form is supported (e.g., correct casing) and document why the alias is used.
- Keep config exception lists (spellchecks, dictionaries, rule overrides) small and scoped. Avoid large catch-all lists; instead, prune them, and for test/local-only terms prefer exclusions or consistent “known words.”

Example (.nvmrc):
```text
# Pin for predictability
v22.2.0

# Or, if using an alias, ensure it matches what nvm supports
lts/iron
```

Example (cspell in ESLint config):
```js
// Don’t let words[] grow unbounded—only keep truly shared terms.
// For test/local-only terms, prefer updating the spelling in code,
// adding targeted ignore patterns, or using exclusions rather than expanding the global list.
```