---
title: Explicit API Contracts
description: 'Treat every cross-boundary API surface (HTTP headers, request/response
  bodies, event projections) as a strict contract: field meaning and inclusion rules
  must be explicit, spec-compliant, and consistently preserved.'
repository: cline/cline#v4
label: API
language: TypeScript
comments_count: 4
repository_stars: 70864
---

Treat every cross-boundary API surface (HTTP headers, request/response bodies, event projections) as a strict contract: field meaning and inclusion rules must be explicit, spec-compliant, and consistently preserved.

Apply these rules:
- Spec-compliant inclusion/exclusion: If a spec requires that a host/tool/event be omitted based on visibility or other attributes, implement that logic unconditionally (no “best-effort” based on feature flags).
- Preserve fields end-to-end: If a field is accepted on input (e.g., displayPrompt), it must be forwarded through every projection/conversion path and included in the corresponding output/event.
- Keep naming aligned with semantics: Don’t silently change what a field/header name means. If the meaning changes, rename (e.g., X-Task-ULID) or send both values.
- Avoid boolean parameters in API-like functions: Replace booleans with an options object using named properties so call sites remain unambiguous.

Example (options object + unambiguous params):
```ts
type LoadOptions = { refresh?: boolean; background?: boolean };

function load(options: LoadOptions = {}) {
  const { refresh = false, background = false } = options;
  // ...
}

// Call site stays self-describing:
load({ refresh: true, background: true });
```

Example (header semantics):
```ts
// Instead of changing the meaning under the old name:
// "X-Task-ID": ulid

// Do one of:
// 1) Keep the original meaning:
"X-Task-ID": taskId

// 2) Rename to match the new meaning:
"X-Task-ULID": ulid

// 3) Send both if needed:
"X-Task-ID": taskId,
"X-Task-ULID": ulid
```