---
title: Bounded Correctness Algorithms
description: 'When implementing algorithmic logic (parsers, estimators, state transitions),
  make correctness and performance constraints explicit: (1) preserve state-window
  invariants across transitions/pagination; (2) canonicalize inputs (paths/CWD) to
  a single representation without breaking roots or literal separators; (3) enforce
  hard bounds (size limits, expansion...'
repository: cline/cline#v28
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70892
---

When implementing algorithmic logic (parsers, estimators, state transitions), make correctness and performance constraints explicit: (1) preserve state-window invariants across transitions/pagination; (2) canonicalize inputs (paths/CWD) to a single representation without breaking roots or literal separators; (3) enforce hard bounds (size limits, expansion depth) and avoid complexity traps (e.g., backtracking regex); (4) validate with targeted edge-case tests plus fuzz/property-style tests for transition/state logic and scenario tests for estimation/parsing.

Practical checklist:
- State/pagination: write the invariants (e.g., “skip removes exactly one row from the pool and visible window only changes as intended”), then add a deterministic sequence test and a fuzz/property test over action verbs.
- Path/CWD: normalize using platform-aware rules but convert to a stable POSIX form only when safe; never collapse filesystem roots (e.g., `/`, `C:\`). Add a test for literal backslashes in filenames.
- Estimation/parsing: ensure the model matches intended semantics (e.g., image estimates should be per-image, not proportional to base64 length). Add tests that assert independence from payload size.
- Bounded work: cap streamed/decoded sizes (archives, extracted content) while reading, cap recursive/link expansion depth, and avoid regex patterns that can backtrack badly on long inputs.

Example (bounded + scenario + invariant test style):
```ts
// 1) Invariants for state transitions (pagination/skip)
// 2) Scenario tests for estimation semantics (image payload size independence)
// 3) Complexity bounds for parsing/install work

// Images: payload length must not move the estimate (flat per-image)
expect(estimateRequestInputTokens({
  messages: [{
    role: 'user',
    content: [{ type: 'image', data: 'A', mediaType: 'image/png' }],
  }],
})).toBe(
  estimateRequestInputTokens({
    messages: [{
      role: 'user',
      content: [{ type: 'image', data: 'A'.repeat(500_000), mediaType: 'image/png' }],
    }],
  })
);

// Parser safety: reject path escapes and cap expansion depth/size during processing.
// (Implementations should normalize to POSIX relative paths, return undefined/skip on escapes,
// and stop expanding links after a fixed max depth.)
```
Apply this standard to any new algorithmic feature: state machines/windows, token/byte estimators, archive/tar parsers, and any path normalization or traversal logic.