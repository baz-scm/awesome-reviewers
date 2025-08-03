---
title: Preserve API compatibility first
description: When modifying existing APIs, maintain backwards compatibility by adding
  new overloads rather than directly changing existing signatures. Mark old signatures
  as deprecated when introducing new patterns, but keep them functional until a major
  version change.
repository: microsoft/typescript
label: API
language: TypeScript
comments_count: 4
repository_stars: 105378
---

When modifying existing APIs, maintain backwards compatibility by adding new overloads rather than directly changing existing signatures. Mark old signatures as deprecated when introducing new patterns, but keep them functional until a major version change.

Example:
Instead of breaking change:
```ts
// Before
function findRenameLocations(fileName: string, position: number, findInStrings: boolean, findInComments: boolean, providePrefixAndSuffixTextForRename?: boolean): RenameLocation[];

// Don't directly modify to:
function findRenameLocations(fileName: string, position: number, findInStrings: boolean, findInComments: boolean, preferences: UserPreferences): RenameLocation[];
```

Add deprecation with overload:
```ts
// Do this instead:
function findRenameLocations(fileName: string, position: number, findInStrings: boolean, findInComments: boolean, preferences: UserPreferences): RenameLocation[];
/** @deprecated Pass `providePrefixAndSuffixTextForRename` as part of a `UserPreferences` object. */
function findRenameLocations(fileName: string, position: number, findInStrings: boolean, findInComments: boolean, providePrefixAndSuffixTextForRename?: boolean): RenameLocation[];
```

This approach:
1. Prevents breaking changes for existing consumers
2. Provides clear migration path through deprecation notices
3. Allows gradual adoption of new patterns
4. Maintains API stability while enabling evolution