---
title: Use descriptive names
description: Choose names that clearly communicate purpose, type, and intent rather
  than generic or ambiguous identifiers. Names should be self-documenting and help
  other developers understand what the code does without additional context.
repository: kilo-org/kilocode
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 7302
---

Choose names that clearly communicate purpose, type, and intent rather than generic or ambiguous identifiers. Names should be self-documenting and help other developers understand what the code does without additional context.

Key principles:
- Use specific names over generic ones (e.g., `filePaths` instead of `files`, `selectedGroupIndex` instead of `selectedGroup`)
- Include action verbs for functions that describe what they do (e.g., `getKiloBaseUri` instead of `KiloBaseUri`)
- Make parameter and variable types clear through naming (e.g., indicate when a string represents a `kilocodeToken`)
- Use full descriptive keys rather than abbreviated suffixes for better searchability

Example improvements:
```typescript
// Instead of generic names:
const cache = new Map<string, Promise<string>>() // unclear what string represents
function KiloBaseUri(options: ApiHandlerOptions) // unclear if this gets, sets, or creates

// Use descriptive names:
const cache = new Map<string, Promise<string>>() // with comment: kilocodeToken -> model promise
function getKiloBaseUri(options: ApiHandlerOptions) // clearly indicates this retrieves a URI

// Parameter clarity:
files?: string[] // ambiguous
filePaths?: string[] // clearly indicates these are file paths
```

This approach reduces cognitive load, improves code maintainability, and makes the codebase more accessible to new team members.