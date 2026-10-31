---
title: Explicit error propagation
description: 'Favor explicit, typed error propagation over implicit or silent failure
  handling. Concretely:


  - Use `Result<T, E>` (or similar) return types to surface success/failure instead
  of throwing just to catch it a few lines later. For example, instead of:'
repository: Helicone/helicone
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 6248
---

Favor explicit, typed error propagation over implicit or silent failure handling. Concretely:

- Use `Result<T, E>` (or similar) return types to surface success/failure instead of throwing just to catch it a few lines later. For example, instead of:
```ts
if (emailResErr) {
  console.error(`Error sending email: ${emailResErr}`);
  throw new Error(emailResErr); // caught outside
}
```
return the error directly: `return err(emailResErr);` and let callers decide how to handle it.

- Never silently fall back to a default when an unexpected/unknown value is encountered (e.g. defaulting an unrecognized provider to `"openai"`). Silent fallbacks hide bugs and produce incorrect behavior downstream; instead, hard-error, log the context (model, provider, request id, etc.), and fail the operation explicitly.

- Make sure `try/catch` blocks actually correspond to code that can throw. If a helper (e.g. a retrying `safePut`) swallows errors internally instead of throwing, the surrounding `catch` is dead code — update the helper to throw/return an error, or remove the misleading catch. Use `console.error` (not `console.log`) when logging failures so they are properly surfaced.

- When an operation's success depends on multiple independent steps (e.g. logging usage and updating a wallet/durable object), don't let one step's failure silently prevent the other from running or from being reported. Run independent steps concurrently, collect each `Result`, and handle/report each error distinctly rather than relying on nested try/catch fallthrough.

- Prefer structured error objects for API-facing errors so callers can return the correct status instead of defaulting to a generic `500`:
```ts
export interface BackendError {
  message: string;      // human-readable message
  details?: string;     // optional debugging detail
  statusCode: number;   // HTTP status to return
}
```

- Keep error branches and their surrounding comments/logs accurate about *why* a branch is being hit (e.g. an `else` branch handling "unsuccessful requests" should not be commented as handling "non-gateway requests"). Misleading context makes debugging production issues much harder.

Applying these practices ensures failures are visible, correctly attributed, and recoverable, rather than being masked by incorrect defaults, dead catch blocks, or throw-to-catch control flow.