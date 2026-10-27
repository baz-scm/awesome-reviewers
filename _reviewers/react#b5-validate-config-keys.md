---
title: Validate config keys
description: Ensure configuration (including tool rule frontmatter and per-fixture
  flags) uses the correct schema and that any overrides are intentional and necessary
  for the behavior you’re testing.
repository: facebook/react#b5
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 251886
---

Ensure configuration (including tool rule frontmatter and per-fixture flags) uses the correct schema and that any overrides are intentional and necessary for the behavior you’re testing.

**1) Use correct config schema keys**
- If your rule system supports path-specific configuration, confirm the frontmatter key matches the documented schema—wrong keys can cause the rule to be silently ignored.

```yaml
---
description: Compiler commit message convention
paths:           # ✅ correct key for path-specific rules
  - "compiler/**"
---
```

**2) Apply only necessary flag overrides in fixtures/tests**
- Don’t add config flags “just because”; add them only when the test would otherwise not exercise the scenario it’s meant to validate.
- If the intent is “this should fail when X is enabled/disabled,” ensure the fixture sets the minimal configuration required to make that failure/pass observable.

```md
```javascript
// @validateNoSetStateInEffects
// @enableAllowSetStateFromRefsInEffects
// @outputMode:"lint"   # ✅ only when needed to make the assertion meaningful
```
```