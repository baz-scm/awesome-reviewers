---
title: Use explicit, consistent names
description: Variable and parameter names should be explicit about their purpose and
  consistent with established naming patterns in the codebase. Avoid ambiguous or
  generic names that could be confusing in context.
repository: nrwl/nx
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 27518
---

Variable and parameter names should be explicit about their purpose and consistent with established naming patterns in the codebase. Avoid ambiguous or generic names that could be confusing in context.

**Make names explicit and descriptive:**
- Use `versionActionsVersion` instead of `version` when the context involves multiple version concepts
- Use `tasksExecutionId` or `executionId` instead of generic `taskId` when referring to execution identifiers
- Use `getAtomizedTaskEnvVars` instead of `getOutputEnvVars` when the function has a specific scope

**Follow established naming conventions:**
- Maintain consistent casing patterns (e.g., `releaseTagPatternStrictPreId` not `releaseTagPatternStrictPreid`)
- Follow existing formatting conventions (e.g., use `is_golden` not `isGolden` when other properties use underscores)

Example:
```typescript
// Avoid: Generic and potentially confusing
const taskId = hashArray([...process.argv, Date.now().toString()]);
const version = getVersion();

// Prefer: Explicit and descriptive  
const tasksExecutionId = hashArray([...process.argv, Date.now().toString()]);
const versionActionsVersion = getVersionActionsVersion();
```