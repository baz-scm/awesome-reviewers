---
title: Explicit undefined state handling
description: Always use explicit, well-defined representations for undefined, uninitialized,
  or invalid states instead of magic values or allowing undefined behavior to propagate
  silently. Create named constants or enum values for undefined states, and make conscious
  decisions about whether to crash, return defaults, or handle undefined values gracefully.
repository: facebook/yoga
label: Null Handling
language: C
comments_count: 5
repository_stars: 18255
---

Always use explicit, well-defined representations for undefined, uninitialized, or invalid states instead of magic values or allowing undefined behavior to propagate silently. Create named constants or enum values for undefined states, and make conscious decisions about whether to crash, return defaults, or handle undefined values gracefully.

Key practices:
1. **Use named constants for defaults**: Instead of hardcoded values like `0.0f`, reference defined constants like `YGDefaultFlexGrow` to prevent bugs and improve clarity
2. **Create explicit undefined representations**: Use static instances like `YGValueUndefined` rather than raw undefined values or magic numbers
3. **Decide on undefined handling strategy**: Choose whether to assert/crash on undefined values (fail-fast) or handle them gracefully, but make this decision explicit
4. **Avoid magic sentinel values**: Instead of using `-1` or other magic numbers to represent invalid states, consider explicit enum values, though weigh API design implications

Example of good practice:
```c
// Good: Named constant for undefined state
static const YGValue YGValueUndefined = {YGUndefined, YGUnitUndefined};
node->style.flexBasis = YGValueUndefined;

// Good: Explicit handling decision
if (YGFloatIsUndefined(baseline)) {
  // Crash fast - undefined baseline indicates a bug
  YGAssert(false, "Baseline function must not return undefined");
}

// Avoid: Magic values
node->style.flexBasis.value = YGUndefined; // Raw undefined
layout->cached_layout.width_measure_mode = (css_measure_mode_t)-1; // Magic -1
```

This approach prevents bugs by making undefined states visible and intentional, while forcing explicit decisions about how to handle edge cases.