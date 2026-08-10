---
title: Use Robust Error Contracts
description: Handle errors in a predictable, maintainable way by (1) ensuring all
  failure-path variables are defined, (2) handling exceptions at one layer (no redundant
  try/catch), (3) validating external data at boundaries with Zod, and (4) using stable
  structured error fields instead of brittle string message matching.
repository: supermemoryai/supermemory
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 28844
---

Handle errors in a predictable, maintainable way by (1) ensuring all failure-path variables are defined, (2) handling exceptions at one layer (no redundant try/catch), (3) validating external data at boundaries with Zod, and (4) using stable structured error fields instead of brittle string message matching.

Apply this standard:
- Compile/runtime safety: don’t reference variables that are only defined in other branches. Prefer computing shared values once (e.g., `const effectiveX = ...`) before divergent logic.
- Single responsibility for exception handling: if a helper already catches/logs, don’t re-catch the same promise at the call site unless you’re adding materially different handling.
- Validate untrusted inputs: when transforming API responses (e.g., social media payloads), validate with Zod (including transforms) before use.
- Stable error contracts: when processing backend responses, branch on `errorCode`/numeric `data`/typed `status` fields rather than matching exact `message` strings.

Example pattern (stable errors + boundary validation):
```ts
import { z } from "zod";

const ResponseSchema = z.object({
  status: z.enum(["ok", "error"]),
  errorCode: z.number().optional(),
  message: z.string().optional(),
  chunkedInput: z.string(),
});

const parsed = ResponseSchema.parse(await vectorSaveResponse.json());
if (parsed.status !== "ok") {
  // Don’t match exact message strings; use a stable code/field.
  if (parsed.errorCode === 123) {
    // handle specific condition
  } else {
    throw new Error(`Memory save failed${parsed.message ? `: ${parsed.message}` : ""}`);
  }
}
```
This reduces runtime failures, prevents inconsistent handling across layers, and makes error-handling logic resilient to message wording changes.