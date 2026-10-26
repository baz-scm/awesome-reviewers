---
title: Semantic Naming for Intent
description: 'Use names that encode intent precisely, and avoid ambiguous/positional
  semantics that make misuse likely.


  Apply these rules:

  - Prefer semantic option objects (or enums) over boolean parameters/fields when
  the meaning isn’t obvious at the call site.'
repository: cline/cline#v1
label: Naming Conventions
language: TypeScript
comments_count: 9
repository_stars: 70862
---

Use names that encode intent precisely, and avoid ambiguous/positional semantics that make misuse likely.

Apply these rules:
- Prefer semantic option objects (or enums) over boolean parameters/fields when the meaning isn’t obvious at the call site.
  - Name for what’s true (positive intent), not via vague terms or negation.
  - Example:
    ```ts
    // Avoid
    // load(refresh: boolean, background?: boolean)

    // Prefer
    await load({ refresh: true, userInitiated: true })
    // or
    await load({ userInitiated: true })
    ```
- Use canonical identifier types/names already present in the codebase (e.g., reuse `ClientName`-style unions instead of inventing parallel string unions).
- Treat telemetry/event payload keys and identifiers as contracts:
  - Keep property names and values aligned everywhere (renames must update all call sites).
  - Prefer object arguments over positional parameters so mismatches are harder to introduce.
- Ensure exported/public APIs are discoverable:
  - Provide a single “obvious” function when possible; otherwise, use names that strongly indicate when to call each one.
- When domain concepts require jargon, either:
  - define the jargon at the module/function level, or
  - choose clearer words that match actual behavior.
- Event/phase naming must not overclaim (e.g., a phase name should reflect what was actually executed vs the ultimate outcome).