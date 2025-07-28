---
title: maintain API backward compatibility
description: When evolving public APIs, prioritize backward compatibility and avoid
  breaking changes to existing interfaces. Support both legacy and new syntax when
  standards evolve, and clearly document any deprecations.
repository: prettier/prettier
label: API
language: JavaScript
comments_count: 4
repository_stars: 50772
---

When evolving public APIs, prioritize backward compatibility and avoid breaking changes to existing interfaces. Support both legacy and new syntax when standards evolve, and clearly document any deprecations.

Key practices:
- Preserve existing public API signatures even when internal implementation changes
- When new standards replace old ones (like import attributes vs assertions), support both syntaxes during transition periods
- Use feature detection and graceful fallbacks rather than removing legacy support immediately
- Add new functionality through optional parameters or separate methods rather than modifying existing signatures

Example from import syntax evolution:
```javascript
// Support both new and legacy syntax
const importAttributesPlugins = ["importAttributes", "importAssertions"];

// Or use parser options to handle both
const keyword = property === "assertions" || node.extra?.deprecatedAssertSyntax ? "assert" : "with";
```

This approach ensures that existing code continues to work while allowing adoption of newer standards, reducing friction for API consumers and maintaining ecosystem stability.