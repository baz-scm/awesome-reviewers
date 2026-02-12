---
title: Prefer utility reuse
description: When changing or adding code prefer existing helpers, language-idiomatic
  constructs, and small well-maintained libraries to keep code DRY, readable, and
  consistent.
repository: likec4/likec4
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 2582
---

When changing or adding code prefer existing helpers, language-idiomatic constructs, and small well-maintained libraries to keep code DRY, readable, and consistent.

Why: Reusing helpers reduces duplication and bugs; using idiomatic patterns (entries, map, pipe) removes boilerplate and conditional checks; consistent literal formats improve readability; standard libraries avoid ad-hoc implementations for common tasks (e.g., color scales).

How to apply (checklist):
- Before adding logic, search for an existing helper or utility and reuse it. Example: replace manual find with an existing helper
  const node = findNodeByElementFqn(context.xynodes, elementFqn)
- Favor idiomatic JS/TS constructs over manual loops and guards. Example: prefer entries or functional pipelines to `for...in` plus manual checks
  for (const [id, styles] of entries(parsedGlobalRules.styles)) { /* ... */ }
  // or
  globalRules.styles = pipe(
    entries(parsedGlobalRules.styles),
    map(([id, style]) => ({ id, style })),
    indexBy(prop('id'))
  )
- Use consistent literal styles for readability: prefer triple-quoted multi-line strings for embedded markdown or long text blocks (match project conventions):
  notes: """
    # Title
    - bullet
  """
- Prefer well-maintained small libraries for common tasks rather than bespoke constants. Example: use @mantine/colors-generator (or an agreed color system like Radix/Open Colors) to produce consistent color scales rather than hand-picking values.

Guidance for code reviews:
- Ask whether new logic duplicates existing helpers; suggest reuse or extraction.
- Recommend idiomatic replacements for loops/conditionals when they simplify code and clarify intent.
- Enforce the project's chosen conventions for string literals and external libraries; prefer standard, vetted solutions for common domains (colors, formatting, parsing).

References: discussions 0, 1, 2, 3.