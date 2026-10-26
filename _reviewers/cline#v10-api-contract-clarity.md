---
title: API Contract Clarity
description: When you change or add API surface area (requests, headers, event envelopes,
  or client helpers), ensure the contract is explicit end-to-end and cannot silently
  change meaning.
repository: cline/cline#v10
label: API
language: TypeScript
comments_count: 5
repository_stars: 70869
---

When you change or add API surface area (requests, headers, event envelopes, or client helpers), ensure the contract is explicit end-to-end and cannot silently change meaning.

Rules:
1) Round-trip new fields through every mapping layer
- If a new input field exists (e.g., `displayPrompt`), carry it through all event copies/projections so it reliably returns to consumers.

2) Don’t change semantic meaning under an existing name
- If a header/field name implies a specific identifier, keep the name aligned with its value. If semantics must change (task id -> ulid), rename the header or send separate headers.

3) Propagate scope/identity explicitly to prevent silent account switching
- Capture required scope/identity in snapshots/tokens and reuse it in subsequent operations instead of re-deriving with potentially different account context.

4) Avoid ambiguous call-site interfaces
- Prefer an options object over positional booleans so the intent is visible at the call site.

5) Avoid parallel flags/logic that can drift
- Derive readiness/config from the shared provider/contract where possible; don’t reintroduce duplicate UI flags that require manual synchronization.

Examples:
- Header semantic change (keep name aligned):
```ts
// Bad: value meaning changed but header name stayed the same
headers["X-Task-ID"] = ulid;

// Better options
headers["X-Task-ID"] = taskId;
headers["X-Task-ULID"] = ulid;
```

- Round-trip field through copies:
```ts
// Ensure envelope -> projection -> handler conversions forward fields
pending_prompt_submitted: {
  displayPrompt: input.displayPrompt,
}
```

- Options object vs boolean parameters:
```ts
load({ refresh: true, background: true });
```