---
title: Validate recursive algorithms against nesting
description: When an algorithm operates on hierarchical or recursive structures (nested
  scopes, nested comprehensions, tree-like state), verify it with multi-level test
  cases, not just the flat/single-level case. Bugs repeatedly surfaced only when a
  second level of nesting was introduced, e.g. a comprehension inside another comprehension
  inside a class body, or a free...
repository: python/cpython
label: Algorithms
language: C
comments_count: 5
repository_stars: 77696
---

When an algorithm operates on hierarchical or recursive structures (nested scopes, nested comprehensions, tree-like state), verify it with multi-level test cases, not just the flat/single-level case. Bugs repeatedly surfaced only when a second level of nesting was introduced, e.g. a comprehension inside another comprehension inside a class body, or a free variable shared between an inlined cell and an enclosing scope; the single-level case looked correct but recursing into children (or climbing to the immediate parent instead of a distant ancestor) was wrong. When adding such logic, write a test with at least two levels of nesting and confirm it matches the pre-existing/reference behavior.

Also, when the same underlying data model is exposed through several related algorithms or accessor methods (e.g. `keys()`, `values()`, `items()`, `__len__()` on a mapping-like view), implement and verify them with one shared traversal/dedup routine so they can't silently disagree on which entries exist or which value is reported for a duplicate name.

Finally, prefer explicit, named representations (lookup tables, named bit masks) over encodings that depend on incidental ordering of a string or array (e.g. deriving a bit position from `strchr("YymdHMSfz", c)`). Implicit-order encodings are fragile to future edits and obscure the algorithm's real decision logic; an explicit table documents intent and survives reordering.

Example of the explicit-encoding fix:
```c
/* Avoid depending on the order of chars in a string. */
static const unsigned int directive_masks[] = {
    ['Y'] = 1 << 0, ['y'] = 1 << 1, ['m'] = 1 << 2, ['d'] = 1 << 3,
    ['H'] = 1 << 4, ['M'] = 1 << 5, ['S'] = 1 << 6,
    ['f'] = 1 << 7, ['z'] = 1 << 8,
};
unsigned int bit = directive_masks[c];
if (bit == 0 || (seen & bit)) {
    return 0;
}
seen |= bit;
```</description>
</invoke>
