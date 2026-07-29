---
title: Domain-aligned Identifier Naming
description: When introducing identifiers that represent external/domain data (e.g.,
  tool calls, event payloads) and shared utilities, keep naming and placement semantically
  aligned and avoid redundant typing.
repository: earendil-works/pi
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 79783
---

When introducing identifiers that represent external/domain data (e.g., tool calls, event payloads) and shared utilities, keep naming and placement semantically aligned and avoid redundant typing.

Apply:
1) Use domain-consistent suffixes for schema-derived types
- If the public shape is named `event.input`, prefer `*Input` (e.g., `BashToolInput`) over `*Params`/`*Parameters` unless the rest of the codebase uses a different established convention.

2) Prefer inference over duplicated/hand-written boundary types
- If a helper returns a generic type from a schema, don’t re-annotate the same structure at the `execute`/handler boundary if the type is already inferred.

3) Put shared utilities in accurately named modules and reuse them
- If multiple parts (e.g., TUI and bash tool) need the same process/shell helper, locate it in the appropriate shared module and ensure the filename reflects its purpose (e.g., `shell.ts` rather than `shell-config.ts` if it’s not config-only).

Example (adapted):
```ts
const bashSchema = Type.Object({
  command: Type.String(),
  timeout: Type.Optional(Type.Number()),
});

// Domain-aligned: matches event.input
export type BashToolInput = Static<typeof bashSchema>;

// Inference-first: avoid re-specifying the same structure if already inferred
export const createBashTool = () =>
  ({
    execute: async (
      _toolCallId: string,
      { command, timeout }, // type inferred from bashSchema
      signal?: AbortSignal,
    ) => {
      // ...
    },
  });
```

Rule of thumb: if the identifier communicates “input/payload”, name it accordingly; if the logic is shared, name the module for what it provides and reuse it rather than duplicating/relocating ad-hoc helpers.