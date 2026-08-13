---
title: API contract clarity
description: Define and document the interface contract for requests/commands so the
  system’s behavior is unambiguous, deterministic, and consistent across call paths
  and modes.
repository: bmad-code-org/bmad-method
label: API
language: Markdown
comments_count: 3
repository_stars: 51859
---

Define and document the interface contract for requests/commands so the system’s behavior is unambiguous, deterministic, and consistent across call paths and modes.

Apply these rules:
- **Gate on explicit intent**: only execute the behavior when the caller’s request clearly triggers it (e.g., the request must literally include/qualify the activation directive). Never “helpfully” run the flow uninvited.
- **Honor forwarded directives**: if your API/workflow passes directives through an internal router/agent, treat a forwarded directive as meeting the same “explicit ask” requirement (don’t accidentally drop the target parameters).
- **Be mode-aware**: interactive callers may ask clarifying questions when intent is unclear; headless/non-interactive callers must not prompt—return a structured refusal/blocked response including the reason.
- **Make overrides and validation deterministic**: for non-interactive parameter setting (CLI/HTTP fields), document:
  - which keys are valid,
  - what happens on unknown keys,
  - how enums are treated,
  - and which actions preserve vs overwrite stored config.
  Warnings are fine, but the persistence/ignore rules must be explicit and consistent.

Example (mode-aware, contract-driven behavior):
```json
{
  "request": "review",
  "mode": "headless",
  "payload": { "diff": "..." }
}
```
Headless response when intent can’t be inferred:
```json
{
  "status": "blocked",
  "reason": "Intent not explicitly specified for review action"
}
```

Checklist for every endpoint/command:
1) What exact inputs qualify as an explicit trigger?
2) Does routing/forwarding preserve those qualifiers and parameters?
3) What are the interactive vs headless behaviors on ambiguity?
4) What is the precise contract for validation, persistence, and action-specific side effects?
5) Are focus hints handled as hints only (never changing scope/meaning)?