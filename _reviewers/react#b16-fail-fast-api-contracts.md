---
title: Fail Fast API Contracts
description: 'When designing or evolving public/shared APIs, make the contract explicit,
  context-safe, and semantically correct.


  Guidelines:

  - **Fail fast on invalid context**: If an API is server-only (or otherwise environment-specific),
  do not export silent no-ops to the wrong runtime. Instead, throw during import/use
  in the invalid context to give immediate feedback.'
repository: facebook/react#b16
label: API
language: JavaScript
comments_count: 6
repository_stars: 251891
---

When designing or evolving public/shared APIs, make the contract explicit, context-safe, and semantically correct.

Guidelines:
- **Fail fast on invalid context**: If an API is server-only (or otherwise environment-specific), do not export silent no-ops to the wrong runtime. Instead, throw during import/use in the invalid context to give immediate feedback.
- **Use schema-friendly, explicit inputs**: Prefer an **options bag** / object-shaped arguments for extensibility and for alignment with tooling schemas. Avoid positional/ambiguous params when adding optional behavior.
- **Keep required semantics required**: Don’t rely on callers/bindings to “implicitly” omit critical parameters. Ensure required fields (e.g., integrity/fetchPriority) are set deliberately or are truly optional in the contract.
- **Match spec semantics and exact values**: When encoding/serializing options or protocol fields, ensure identity keys and string values match the governing standard; add tests for edge cases.
- **Control mode explosion**: If interface growth introduces multiple behavioral variants, prefer **separate variants** (or clearly discriminated options) over ever-widening argument lists that obscure when/why each field is used.

Example pattern (context-safe boundary):
```js
// server-only module
export function createMaskLedger() { /* ... */ }

// client entry (intentionally throws)
throw new Error("createMaskLedger is server-only; import from the server entry point.");
```

Example pattern (schema-friendly options bag):
```ts
type GetComponentArgs = { uid: string, includeHooks?: boolean };
function getComponentByUid(args: GetComponentArgs): NodeInfo | ToolError;
```