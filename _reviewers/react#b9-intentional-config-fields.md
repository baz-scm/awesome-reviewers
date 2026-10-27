---
title: Intentional Config Fields
description: 'When changing configuration files or config-bearing fixtures (feature
  flags, rule frontmatter, test metadata), ensure two things: (1) the config uses
  the correct schema/keys so it is actually applied, and (2) the config is set intentionally
  so the test or behavior under change is truly exercised.'
repository: facebook/react#b9
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 251891
---

When changing configuration files or config-bearing fixtures (feature flags, rule frontmatter, test metadata), ensure two things: (1) the config uses the correct schema/keys so it is actually applied, and (2) the config is set intentionally so the test or behavior under change is truly exercised.

Checklist:
- Match documented config/frontmatter keys exactly (wrong keys can silently disable the intended behavior).
- For fixtures/tests, don’t remove explicit config fields just because the current run passes—keep them when they’re there to force the validation/behavior path the test is meant to cover.

Example (fixing misnamed frontmatter key):
```yaml
---
description: Compiler commit message convention
paths:   # correct key for path-specific rules
  - 'compiler/**'
---
```

Example (keeping explicit test config when it drives validation):
```md
```javascript
// @validateNoSetStateInEffects
// @enableAllowSetStateFromRefsInEffects
// @outputMode:"lint"
```
```