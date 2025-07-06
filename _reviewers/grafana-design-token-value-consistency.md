---
title: Design token value consistency
description: When implementing design tokens in code, ensure values accurately represent
  the intended visual outcome, even if design tools have limitations. Use proper unit
  types that correctly translate to UI rendering rather than arbitrary numeric values.
repository: grafana/grafana
label: Code Style
language: Json
comments_count: 3
repository_stars: 68825
---

When implementing design tokens in code, ensure values accurately represent the intended visual outcome, even if design tools have limitations. Use proper unit types that correctly translate to UI rendering rather than arbitrary numeric values.

For example, when defining border-radius tokens for circular elements, use:
```json
"circle": {
  "value": "100%",
  "type": "borderRadius",
  "description": "Used to generate full circle elements"
}
```

Instead of using large numeric values like `100000` which may not scale properly with element dimensions.

While maintaining comprehensive token scales for future flexibility is valuable, clearly document which tokens are intended for direct use versus internal reference. Add descriptive comments that explain the purpose and usage context of each token group. This improves code readability and prevents misapplication of foundation-level tokens that should only be referenced by semantic tokens.