---
title: Explicit endpoint contract composition
description: Define each endpoint's request/response contract explicitly rather than
  deriving it by inheriting another endpoint's full schema and subtracting or layering
  fields on top. Extend-then-omit composition (e.g., building a Responses schema by
  starting from the entire Chat schema and omitting fourteen fields, or extending
  a full provider config into a...
repository: promptfoo/promptfoo
label: API
language: TypeScript
comments_count: 7
repository_stars: 26565
---

Define each endpoint's request/response contract explicitly rather than deriving it by inheriting another endpoint's full schema and subtracting or layering fields on top. Extend-then-omit composition (e.g., building a Responses schema by starting from the entire Chat schema and omitting fourteen fields, or extending a full provider config into a client-only schema) silently grants new fields to endpoints that never decided to support them, and lets unrelated data (like a pricing/catalog table) drive request-shape decisions. Instead:

- Extract the truly shared fields/capabilities into a base schema, then compose each endpoint by positively selecting (`.pick`/explicit allowlist) the fields it actually supports.
- Make capability/behavior decisions (token fields, sampling support, reasoning support, etc.) an explicit, named policy rather than inferring them from membership in an unrelated table.
- Ensure the contract accurately mirrors what the implementation actually does: don't accept config fields that are silently ignored at runtime (e.g., accepting `defaultArgs`/`transformResponse` in a schema whose client never implements them), and don't reject native fields the underlying API/SDK actually supports.
- Validate that externally-facing contracts (public schemas, OpenAPI docs, exported types) compose with the real execution boundary — add a test that constructs the runtime object from the parsed/validated input — and that documented restrictions are actually enforced by the route/handler, not just described.

Example of the problem to avoid:
```ts
// Bad: Responses inherits Chat's entire option set, then subtracts fields.
export const ResponsesConfigSchema = ChatConfigSchema.omit({ tool_resources: true, ... });

// Good: compose explicitly from shared + endpoint-specific allowlists.
const SharedFields = TextFields.pick({ temperature: true, max_tokens: true, ... });
export const ResponsesConfigSchema = SharedFields.extend({ /* Responses-only fields */ });
```
Applying this consistently prevents accidental field leakage between endpoints, keeps capability logic traceable to an explicit decision, and keeps published contracts truthful about what the API actually accepts and enforces.