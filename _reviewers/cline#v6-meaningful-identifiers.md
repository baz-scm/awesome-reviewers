---
title: Meaningful identifiers
description: 'Use naming that encodes real meaning and preserves API/contract clarity.


  Guidelines:

  - Prefer domain-specific, positive semantics over vague names and negation. If a
  flag really means “user initiated,” name it `userInitiated` (not `!background` /
  ambiguous `background`).'
repository: cline/cline#v6
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70864
---

Use naming that encodes real meaning and preserves API/contract clarity.

Guidelines:
- Prefer domain-specific, positive semantics over vague names and negation. If a flag really means “user initiated,” name it `userInitiated` (not `!background` / ambiguous `background`).
- Avoid boolean fields for domain situations that have distinct meanings. When the state has multiple interpretations, model it as a discriminated union or string-literal enum with explicit positive names (e.g., `entry?: "run" | "continue"`, `promptSeeded?: boolean` → better: `promptSource?: "seeded" | "written"`).
- Keep names consistent with the identifier’s content across events and transport layers. If you change from `taskId` to `ulid`, update both the property key and all call sites, and ensure join keys aren’t silently mixed under the same field name.
- Treat “identifier naming” as part of cross-layer contracts: if header names imply meaning (e.g., `X-Task-ID`), either keep the value aligned with the name or rename the header (e.g., `X-Task-ULID`) / send both explicitly.
- Don’t introduce jargon or unclear metaphors in identifiers/comments. If the team uses internal metaphors (e.g., “pointer,” “dangling”), ensure naming is paired with an explanatory contract.

Example (before → after):
```ts
// Before: positional rename bug compiles but breaks meaning
captureCheckpointUsage(taskId, "commit_created", durationMs); // taskId passed to ulid slot

// After: name keys/props to match the identifier actually carried
captureCheckpointUsage(ulid, "commit_created", durationMs);
// and keep the captured property name consistent with the identifier type
properties: { ulid, action, durationMs }
```

Also apply to flags:
```ts
const load = (userInitiated: boolean) => {
  if (userInitiated) showInitialSpinner();
};
```

Net effect: names should be unambiguous, reflect the actual data/state carried, and stay correct across call sites, telemetry/event schemas, and external headers.