---
title: Guard nullable values
description: Always check for null/undefined before accessing values or rendering
  UI instead of relying on non‑null assertions or unconditional usage. Prefer optional
  chaining and explicit guards in logic and conditional rendering in JSX.
repository: likec4/likec4
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 2582
---

Always check for null/undefined before accessing values or rendering UI instead of relying on non‑null assertions or unconditional usage. Prefer optional chaining and explicit guards in logic and conditional rendering in JSX.

Why: Non-null assertions (`!`) and unconditional rendering can cause runtime exceptions when data is absent. Explicit checks make intent clear and avoid crashes.

How to apply:
- Replace `!` assertions with optional chaining and guards:
  - Bad: let relationId = only(edge.data.relations)!.id;
  - Good: let relationId = only(edge.data.relations)?.id;
           if (relationId) { /* use relationId */ }

- Conditionally render components only when required data exists:
  - Bad: <LikeC4CustomColors customColors={view.customColorDefinitions} />
  - Good: {view.customColorDefinitions && (
      <LikeC4CustomColors customColors={view.customColorDefinitions} />
    )}

Notes:
- Use optional chaining (?.) when a property may be undefined; follow with an if-check if you need to act on the value.
- For JSX, prefer conditional rendering or early returns to avoid passing undefined props or rendering components that expect data.
- Reserve `!` only when you can guarantee the value (and document why). When in doubt, guard. 