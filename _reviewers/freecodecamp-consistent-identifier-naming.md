---
title: Consistent Identifier Naming
description: 'When updating curriculum challenges or UI code, ensure all identifiers
  are spelled, cased, and named consistently across: the prompt, hints, and what tests/DOM
  queries expect. Also use framework-correct attribute names (e.g., JSX `className`)
  and semantic, descriptive labels for user-facing accessibility (e.g., informative
  `alt` text).'
repository: freeCodeCamp/freeCodeCamp
label: Naming Conventions
language: Markdown
comments_count: 8
repository_stars: 444449
---

When updating curriculum challenges or UI code, ensure all identifiers are spelled, cased, and named consistently across: the prompt, hints, and what tests/DOM queries expect. Also use framework-correct attribute names (e.g., JSX `className`) and semantic, descriptive labels for user-facing accessibility (e.g., informative `alt` text).

**Checklist**
- **Exact name matching:** If instructions mention `utilitiesNumberInputs`, but tests assert `utilitiesInputs`, make the instruction/hint match the actual variable name used/required.
- **Correct JSX/DOM attribute names:** In JSX/TSX use `className` (not `class`).
- **Descriptive user-visible naming:** For images, don’t use vague alt text like `"Player"`; name what’s actually shown.
- **Casing and function naming:** Keep function names consistent with the expected casing (e.g., `getLongestSubstring`).
- **Signature clarity:** When type annotations are required by tests, make the function signature match the expected parameter name and type annotation (and don’t introduce distractor typos like `renderMotorCycleCard` vs `renderMotorcycleCard`).

**Example**
```js
// JSX/TSX: use className
return <img src=".../pele.jpg" alt="Pelé headshot" className="card-image" />;

// Spec/tests: ensure variable names match exactly
const utilitiesInputs = document.querySelectorAll("#utilities input[type='number']");
```