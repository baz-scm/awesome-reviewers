---
title: Prefer Shared, Role-Based Code
description: 'When implementing new functionality, favor maintainability patterns
  over local duplication and scattered conditionals.


  - **Reuse existing “source of truth” utilities**: If core/shared already normalizes/validates
  data (git remotes/refs, shell detection, session title inference), call that instead
  of re-implementing the logic in an app or adding parallel...'
repository: cline/cline?x=1
label: Code Style
language: TypeScript
comments_count: 8
repository_stars: 70861
---

When implementing new functionality, favor maintainability patterns over local duplication and scattered conditionals.

- **Reuse existing “source of truth” utilities**: If core/shared already normalizes/validates data (git remotes/refs, shell detection, session title inference), call that instead of re-implementing the logic in an app or adding parallel helpers.
  - Example: remove a local `isPowerShellCommand()` if `getShellKind()` already covers it.

- **Avoid conditional sprawl with roles/factories**: If behavior depends on configuration (e.g., output mode), create the appropriate outputter once and make lifecycle calls straight-line.
  ```ts
  interface RunOutputter {
    runStarted(meta: unknown): void;
    runResult(result: unknown): void;
    runAborted(err: unknown): void;
  }

  function createRunOutputter(mode: "json" | "console", verbose: boolean): RunOutputter {
    return mode === "json" ? new JsonRunOutputter(verbose) : new ConsoleRunOutputter(verbose);
  }

  const outputter = createRunOutputter(config.outputMode, config.verbose);
  outputter.runStarted(sessionMeta);
  // ... straight-line lifecycle dispatch
  ```

- **Model state with unions, not booleans**: Prefer string unions (or discriminated unions) to represent multiple valid modes and prevent invalid combinations.
  - Example: use `resumed?: "resumed" | "fresh"` (or similar) instead of `resumed?: boolean`.

- **Consolidate similar formatters**: If two functions share the same trimming/escaping/wrapping logic but differ slightly, unify them behind a discriminated union and keep escaping rules in one place.

- **Eliminate redundant helpers and imports**: Remove local wrappers and unused imports when shared equivalents exist.

- **Replace magic numbers with named constants + intent docs**: For timeouts/fallbacks (especially around async cleanup), extract constants and document the rationale (e.g., “grace period for draining output after process exit”).
  ```ts
  const EXIT_DRAIN_GRACE_MS = 1000; // grace period to drain output after exit
  ```