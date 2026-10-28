---
title: Eliminate duplicate logic
description: Before writing new logic, search the codebase (including shared/core
  packages) for an existing implementation and reuse or extend it rather than re-deriving
  the same behavior. When review reveals that two or more code paths already do the
  same thing with minor variations, consolidate them into one shared function/method
  and let callers supply only the parts...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Code Style
language: TypeScript
comments_count: 9
repository_stars: 70965
---

Before writing new logic, search the codebase (including shared/core packages) for an existing implementation and reuse or extend it rather than re-deriving the same behavior. When review reveals that two or more code paths already do the same thing with minor variations, consolidate them into one shared function/method and let callers supply only the parts that actually differ, instead of keeping parallel near-duplicates with copy-pasted comments.

Place shared logic in the layer where it belongs so it can be reused, respecting the dependency graph (e.g., utilities usable by multiple apps belong in a shared/core package, not duplicated inside one app; apps may depend on core, but core must never depend on an app). If a block of logic is specific to one concern (e.g., a particular tool) and is growing large inside a general-purpose file, extract it into its own focused module rather than letting it bloat a shared file.

Example — reuse an existing shared helper instead of reimplementing it:

```ts
// Before: reimplementing shell detection locally
export function isPowerShellCommand(command: string[]): boolean {
  const base = win32.basename(command[0]).toLowerCase();
  return base === "powershell" || base === "pwsh" /* ... */;
}

// After: reuse the existing utility from @cline/shared
import { getShellKind } from "@cline/shared";
const isWinPowerShell =
  process.platform === "win32" && getShellKind(command[0]) === "powershell";
```

Applying this consistently keeps the codebase smaller, easier to navigate, and ensures bug fixes or behavior changes only need to happen in one place.