---
title: Semantic and Consistent Naming
description: Use naming that is (a) semantically self-evident, (b) consistent with
  shared/canonical identifiers, and (c) safe across boundaries like telemetry schemas.
repository: cline/cline#v28
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70892
---

Use naming that is (a) semantically self-evident, (b) consistent with shared/canonical identifiers, and (c) safe across boundaries like telemetry schemas.

**Standards**
1. **Reuse canonical identifier types/sources**
   - Prefer shared types/constants (e.g., `ClientName`) over ad-hoc strings.
   - When a value is displayed vs used operationally (e.g., repo/remote selection), ensure both follow the same rule so names don’t diverge from behavior.

2. **Name by meaning, not by vague intent**
   - Avoid parameter names that hide what the boolean/string actually represents. If a flag changes behavior based on user intent/state, encode that intent/state in the name.

3. **Avoid ambiguous booleans for domain states**
   - If a boolean implies a multi-meaning state (or requires reading negation logic), replace it with a descriptive union/enum string.

   Example (preferred):
   ```ts
   type EntryKind = "run" | "continue";
   function beforeRun(ctx: { entry: EntryKind; promptSeedState: "seeded" | "written" }) {}
   ```

4. **Treat schema/key renames as breaking changes**
   - When renaming telemetry/event property keys or function parameters that map to them, update all call sites. Avoid positional-only renames where TypeScript can’t help; prefer object parameters to make mismatches obvious.

5. **Don’t rely on unexplained jargon in names/comments**
   - If you use metaphors like “pointer/dangling/save”, define them explicitly and consistently with the code’s actual behavior.

6. **Make exported APIs hard to choose wrong**
   - Prefer one primary exported function that everyone uses.
   - If multiple exports are necessary, name them so the intended caller decision is obvious (and ensure comments remove ambiguity).