---
title: Meaningful Identifier Naming
description: Adopt a naming standard where identifiers and public APIs make their
  intent unambiguous, reflect domain meaning, and remain consistent across the system.
repository: cline/cline#v16
label: Naming Conventions
language: TypeScript
comments_count: 8
repository_stars: 70882
---

Adopt a naming standard where identifiers and public APIs make their intent unambiguous, reflect domain meaning, and remain consistent across the system.

Rules:
1) Prefer intention-revealing names over vague flags and generic words
- Avoid boolean parameters whose meaning isn’t obvious (e.g., `background`). Use names that state the positive condition, e.g. `userInitiated`.
- Avoid internal jargon that requires reading code to understand (e.g., “pointer/save/dangling”) unless the file/module clearly defines it.

2) Don’t use boolean fields for domain states—use descriptive enums/strings
- If a boolean represents a meaningful state distinction, replace it with a string/enum that names the states positively (e.g., `entry: "run" | "continue"` rather than `promptSeeded?: boolean`).

3) Enforce existing casing/convention rules based on identifier origin
- If your codebase uses different casing depending on who supplies the key, keep that rule consistent (e.g., caller-supplied `context` keys in `camelCase`, envelope/global enrichment in `snake_case`).

4) Make exported APIs easy to choose
- If multiple exported functions exist, their names should help developers pick the right one. If the choice is subtle, consider exporting one obvious entry point (and optionally keep others private or clearly labeled for testing/internal use).

5) When renaming identifiers/properties, update all call sites and keys
- Renames can be “type-safe” but still wrong when arguments are positional (TypeScript won’t catch it). Ensure both the parameter name and the corresponding property key are updated together everywhere the helper is called.

Example (boolean → enum/string):
```ts
type Entry = "run" | "continue";

interface AgentRunLifecycleContext {
  entry?: Entry;
  // instead of: promptSeeded?: boolean
}
```

Example (vague flag → positive name):
```ts
const load = useCallback(async (refresh: boolean, userInitiated = false) => {
  // ...
}, []);
```