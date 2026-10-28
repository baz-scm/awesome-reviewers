---
title: Fail-safe state transitions
description: 'When code performs multi-step state changes (installs, renames, overwrites),
  design for interruption and failure up front rather than bolting on recovery later.
  Prefer the simplest fail-safe design: avoid risky swap-and-delete sequences when
  possible (e.g. only publish a staged bundle when no destination exists yet, instead
  of renaming the old one away and...'
repository: ogulcancelik/herdr#canary966c66ad
label: Error Handling
language: Python
comments_count: 4
repository_stars: 46332
---

When code performs multi-step state changes (installs, renames, overwrites), design for interruption and failure up front rather than bolting on recovery later. Prefer the simplest fail-safe design: avoid risky swap-and-delete sequences when possible (e.g. only publish a staged bundle when no destination exists yet, instead of renaming the old one away and renaming the new one in) so a crash or power loss can never leave a half-replaced or corrupted artifact. If a multi-step transition truly cannot be avoided, make it explicitly recoverable: write a well-named backup/marker before mutating, and have the next run detect and restore it before doing any other work, with a test that simulates interruption between the steps.

Never silently overwrite, delete, or merge into caller-provided or pre-existing state — fail loudly instead. For example, if an output directory already exists, raise an error rather than overwriting it; the caller must explicitly clean up or choose a new path, since silent destructive behavior is more dangerous than a hard failure.

Likewise, validate inputs and preconditions strictly before indexing, bitwise operations, or other assumptions are applied to them. Malformed or incomplete data (e.g. a record that isn't exactly the expected shape/length) must not be processed as if it were valid — treat it as a distinct "inconclusive"/error status with a clear reason, and add test coverage for these malformed-input paths, rather than letting the code crash or silently produce wrong results.

In short: eliminate unsafe partial-state windows where possible, make unavoidable ones explicitly recoverable and tested, and always prefer loud, explicit failures or clearly-labeled degraded statuses over silent corruption or incorrect success.