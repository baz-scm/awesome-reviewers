---
title: Semantic naming rules
description: 'Use names that reveal intent at the call site, keep them consistent
  via shared types/keys, and avoid “meaningless” booleans/flags.


  Practical guidelines:'
repository: cline/cline#v10
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70869
---

Use names that reveal intent at the call site, keep them consistent via shared types/keys, and avoid “meaningless” booleans/flags.

Practical guidelines:
1) Prefer domain-state naming over vague booleans
- If the domain has more than two meaningful states, replace boolean flags with a descriptive string union (positive wording beats negation).

```ts
// Prefer
type Entry = "run" | "continue";
entry?: Entry;

// Over vague boolean
// isSeeded?: boolean; // unclear what “false” means
```

2) Rename parameters so callers don’t mentally invert logic
- If you pass `!background`, the name should reflect what it actually represents (e.g., `userInitiated`).

3) Keep identifiers/keys consistent across systems
- When using shared naming sources (e.g., `ClientName` unions, telemetry property keys), derive from the shared type/union rather than duplicating strings.
- When renaming event properties (e.g., `taskId` → `ulid`), update all positional call sites or you will end up emitting mixed formats under the same key.

4) Name async APIs around usage
- For awaitable values, prefer naming that reads well with `await` (e.g., make the promise/value the thing you await, rather than `whenX().then(...)`).

5) Remove or define jargon
- If a file uses non-obvious terms (“pointer”, “dangling”, “save”), add a short top-level explanation and/or clarify each function’s “what/why/caveats” so readers don’t have to reverse-engineer the domain model.