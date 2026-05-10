---
title: Config must be consistent
description: Ensure every rendering/utility path uses the correct configuration *namespace*
  and that config values are passed explicitly (not implicitly via global getters
  or captured/stale variables).
repository: mermaid-js/mermaid
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 87952
---

Ensure every rendering/utility path uses the correct configuration *namespace* and that config values are passed explicitly (not implicitly via global getters or captured/stale variables).

Practical rules:
- **Match config paths end-to-end**: if tests set `config.flowchart.htmlLabels`, the code that affects label sizing must read the same path (and the same key name).
- **Don’t pull config inside internal helpers**: prefer passing `config`/needed flags as parameters so helpers are deterministic and easy to test.
- **Avoid caching/stale config snapshots**: don’t compute `const conf = getConfig().<section>` once if it can be initialized later; fetch/use config at the correct lifecycle or keep the prior approach.
- **Use diagram-specific defaults**: when computing defaults for a diagram/module, read from its own config section (e.g., block defaults from `config.block`, not `config.flowchart`).

Example pattern (config injection):
```ts
// Bad: internal utility reaches out to global config
import { getConfig } from '../config.js';
function preprocessMarkdown(markdown: string) {
  const markdownAutoWrap = getConfig().markdownAutoWrap;
  // ...
}

// Good: pass only what you need
function preprocessMarkdown(markdown: string, markdownAutoWrap: boolean) {
  // ...
}

// Call site
const { markdownAutoWrap } = getConfig();
preprocessMarkdown(markdown, markdownAutoWrap);
```