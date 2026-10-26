---
title: Centralize shared logic
description: When code touches shared behavior (git checks, shell detection, formatting/escaping,
  session/output lifecycle), don’t duplicate it locally via ad-hoc helpers or repeated
  conditional branches.
repository: cline/cline#v2
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70861
---

When code touches shared behavior (git checks, shell detection, formatting/escaping, session/output lifecycle), don’t duplicate it locally via ad-hoc helpers or repeated conditional branches.

Apply these rules:

- Reuse existing core/shared utilities first. If logic already exists in core/@cline/shared (e.g., remote normalization, shell kind detection), import and call it rather than re-implementing.
- Centralize “shared rules” (format/escaping/wrapping) in one place. If you need a new variant (tool vs run-start, etc.), extend the existing formatter using a discriminated union so escaping lives only once.
- Replace scattered output-mode conditionals with a role/interface created once (factory). Keep lifecycle events as straight calls (runStarted/runResult/runAborted), and let each outputter decide what to render.
- Model state with expressive types. Prefer string/discriminated unions over boolean flags to prevent invalid combinations and make intent/test cases clearer.

Example (role-based output + union state):

```ts
type ResumeState = "new" | "resumed";

interface RunOutputter {
  runStarted(args: { resumeState: ResumeState }): void;
  runResult(result: unknown): void;
  runAborted(err: unknown): void;
}

class JsonRunOutputter implements RunOutputter {
  constructor(private verbose: boolean) {}
  runStarted({ resumeState }: { resumeState: ResumeState }) {
    // emit JSON
  }
  runResult(result: unknown) { /* ... */ }
  runAborted(err: unknown) { /* ... */ }
}

class ConsoleRunOutputter implements RunOutputter {
  constructor(private verbose: boolean) {}
  runStarted({ resumeState }: { resumeState: ResumeState }) {
    // emit console
  }
  runResult(result: unknown) { /* ... */ }
  runAborted(err: unknown) { /* ... */ }
}

function createOutputter(outputMode: "json" | "console", verbose: boolean): RunOutputter {
  return outputMode === "json"
    ? new JsonRunOutputter(verbose)
    : new ConsoleRunOutputter(verbose);
}
```

Use this standard to reduce duplication, improve readability, and make behavior consistent across the codebase.