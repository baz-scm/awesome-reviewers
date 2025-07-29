---
title: Multi-indicator configuration detection
description: When detecting configuration states, use multiple indicators rather than
  relying on a single source of truth, especially when dealing with ambiguous or transitional
  states. Provide clear documentation explaining the detection logic and reasoning
  behind each check.
repository: sveltejs/svelte
label: Configurations
language: JavaScript
comments_count: 3
repository_stars: 83580
---

When detecting configuration states, use multiple indicators rather than relying on a single source of truth, especially when dealing with ambiguous or transitional states. Provide clear documentation explaining the detection logic and reasoning behind each check.

Configuration detection often requires examining multiple signals because:
- Single indicators can be misleading (e.g., tsconfig.json presence doesn't guarantee TypeScript usage)
- Transitional states may need special handling (e.g., "maybe_runes" mode)
- Legacy compatibility requires fallback detection methods

Example from TypeScript detection:
```javascript
uses_ts:
    // Some people could use jsdoc but have a tsconfig.json, so double-check file for jsdoc indicators
    (use_ts && !source.includes('@type {')) ||
    !!parsed.instance?.attributes.some(
        (attr) => attr.name === 'lang' && attr.value[0].data === 'ts'
    )
```

Example from runes mode detection:
```javascript
// Components not explicitly in legacy mode might be expected to be in runes mode (especially since we didn't
// adjust this behavior until recently, which broke people's existing components), so we also bail in this case.
// Kind of an in-between-mode.
if (context.state.analysis.runes || context.state.analysis.maybe_runes) {
```

Always document the rationale behind complex detection logic, particularly when handling edge cases or backward compatibility scenarios.