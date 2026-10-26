---
title: Use explicit roles
description: 'Prefer clear abstractions and explicit types over duplicated logic and
  scattered conditionals.


  Apply these rules:

  - Reuse existing shared/core utilities for common behavior (don’t re-implement checks
  like git/shell detection in app code; move shared logic into core when needed).'
repository: cline/cline#v23
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70889
---

Prefer clear abstractions and explicit types over duplicated logic and scattered conditionals.

Apply these rules:
- Reuse existing shared/core utilities for common behavior (don’t re-implement checks like git/shell detection in app code; move shared logic into core when needed).
- Replace boolean flags with a string union (or discriminated union) when multiple states exist—avoid invalid combinations.
- Avoid threading `if (outputMode === "json") ... else ...` through the code. Initialize a single mode-appropriate object (e.g., `RunOutputter`) once, then call consistent lifecycle methods.
- Centralize repeated formatting/escaping logic in one place (use a discriminated union to emit different attributes only where applicable).
- Eliminate magic numbers/unnecessary imports; extract constants (with brief intent docs) and rely on shared helpers.

Example (role + union):
```ts
type OutputMode = "json" | "console";

type SessionState =
  | { resumed: false }
  | { resumed: true };

interface RunOutputter {
  runStarted(): void;
  runResult(result: unknown): void;
  runAborted(error: Error): void;
}

function createOutputter(mode: OutputMode, verbose: boolean): RunOutputter {
  return mode === "json"
    ? new JsonRunOutputter({ verbose })
    : new ConsoleRunOutputter({ verbose });
}

export async function runAgent(mode: OutputMode, verbose: boolean, state: SessionState) {
  const outputter = createOutputter(mode, verbose);
  outputter.runStarted();
  // ...
}
```

Outcome: code becomes easier to read, test, and extend—new states/modes add new union members/outputter implementations instead of multiplying conditionals and duplicated helpers.