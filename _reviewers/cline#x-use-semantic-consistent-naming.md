---
title: Use semantic consistent naming
description: Adopt names that precisely describe meaning (not mechanism), follow the
  project’s canonical identifier types, and preserve “meaning contracts” across call
  sites—especially for telemetry/analytics keys.
repository: cline/cline#x
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 70861
---

Adopt names that precisely describe meaning (not mechanism), follow the project’s canonical identifier types, and preserve “meaning contracts” across call sites—especially for telemetry/analytics keys.

Apply these rules:
- Prefer intent-revealing names over vague ones. If the name encodes the real decision, update it (e.g., `background` -> `userInitiated` when it’s the user-triggered gate).
- Avoid booleans for multi-meaning domains. If the concept has distinct states, model them as a positive enum/string (e.g., `promptSeeded` becomes something like `promptInput: "seeded" | "written"`).
- Standardize identifiers using shared canonical types. Don’t use ad-hoc strings when a shared `ClientName` (or equivalent) exists—extend the shared type instead.
- Treat naming changes as contract changes: for telemetry/analytics properties, rename with full call-site propagation and ensure the same key carries the same identifier format across events (positional args can silently compile).
- Make exported/public helpers obvious to choose. If multiple functions exist, ensure the names (and/or docs) make the intended call-site decision unambiguous.
- For status/phase labels, name what the phase *claims* to represent (avoid names that invite incorrect interpretations).

Example:
```ts
// Prefer enums over boolean negation
type PromptOrigin = "seeded" | "written";

interface Ctx {
  entry?: "run" | "continue";
  promptOrigin?: PromptOrigin; // replaces promptSeeded boolean
}

// Prefer canonical identifiers
type ClientName = "cline-cli" | "cline-desktop" | "cline-vscode" | "cline-jetbrains";

function buildClient(client: ClientName) {
  // ...
}

// Telemetry rename must update all call sites
// captureCheckpointUsage(ulid: string, ...)
// and call sites must pass the ulid, not the task id.
```