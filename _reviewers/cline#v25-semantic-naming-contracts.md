---
title: Semantic naming contracts
description: 'Names must communicate the real contract: what a value represents, what
  state it encodes, how long it’s stable, and what a label/event *claims*.


  Apply these rules in naming reviews:'
repository: cline/cline#v25
label: Naming Conventions
language: TypeScript
comments_count: 9
repository_stars: 70891
---

Names must communicate the real contract: what a value represents, what state it encodes, how long it’s stable, and what a label/event *claims*.

Apply these rules in naming reviews:
1) Prefer explicit state names over booleans when the meaning isn’t a true yes/no.
   - Bad: `promptSeeded?: boolean`
   - Better: `entry?: 'run' | 'continue'`, `promptOrigin?: 'seeded' | 'written'`

2) Make identifiers match lifetime/usage. If something is referenced over an entire turn, its id should be stable for that scope.
   - Example pattern: build a row id from the turn’s first-set revision so Skip/Undo keep pointing at the same row.

3) Ensure renames are schema-consistent end-to-end, especially for telemetry/event properties.
   - If `taskId` → `ulid`, update all call sites; positional args can compile while producing wrong semantic joins.

4) Standardize against shared naming sources (types/enums/constants) rather than ad-hoc strings.
   - Example: use the shared `ClientName`/host identifiers instead of new unaligned string literals.

5) Don’t “normalize” casing blindly—follow the existing rule by key origin/source (e.g., `context` caller-supplied keys vs telemetry envelope/global-enrichment keys).

6) Keep phase/status wording honest: labels must reflect what the phase actually does/knows (e.g., rename “completed” to “retried” if it no longer judges outcome).

7) For exported APIs, choose names that help consumers pick the right one (or export only one obvious entry point); avoid vague/competing names without strong hints and guidance comments.

If a name would cause a developer to infer the wrong behavior/outcome, treat it as a naming bug and fix it in the next iteration.