---
title: API contract consistency
description: Treat every field, flag, and header in a public or inter-service API
  as a contract that other integrators will depend on, and design it to stay accurate,
  symmetric, and non-redundant over time.
repository: cline/cline#;sleep 4;
label: API
language: TypeScript
comments_count: 6
repository_stars: 70976
---

Treat every field, flag, and header in a public or inter-service API as a contract that other integrators will depend on, and design it to stay accurate, symmetric, and non-redundant over time.

- Name fields/headers for what they actually carry, and never silently repurpose them. Changing `X-Task-ID` to send a ulid instead of the task id broke the contract without any signal to consumers; if the meaning changes, rename the field (e.g. `X-Task-ULID`) or add a new one.
- Prefer string unions (or small enums) over booleans for state that models more than a simple on/off switch, e.g. `resumed?: "resume" | "start"` instead of `resumed?: boolean`. Booleans proliferate and make invalid state combinations easy to create and hard to test.
- Keep inputs and outputs symmetric: if a field can be set on a request/event (e.g. `displayPrompt`), make sure every related response/event that echoes that data forwards it back out. A field that goes in and never comes out is a trap for the next integrator, even if no current caller depends on it yet.
- Don't duplicate information that already exists in a shared/canonical contract (e.g. provider catalog readiness) by adding a second ad-hoc flag on another type. Extend the shared contract instead so all consumers read the same source of truth and avoid synchronization bugs.
- Before publishing a new option on an SDK/client surface, prefer making spec-correct behavior unconditional rather than adding a flag to toggle it. Extra flags are cheap to avoid before release and expensive to remove afterward.

Example — before/after for the header bug above:
```ts
// Before: name says "task id", value is actually the ulid.
defaultHeaders: { "X-Task-ID": this.options.ulid || "" }

// After: name matches content, or send both explicitly.
defaultHeaders: {
  "X-Task-ID": this.options.taskId || "",
  "X-Task-ULID": this.options.ulid || "",
}
```