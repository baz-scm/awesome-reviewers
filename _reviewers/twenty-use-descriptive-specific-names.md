---
title: Use descriptive specific names
description: Names should be descriptive and specific enough to clearly communicate
  their purpose and avoid confusion. This includes using full words instead of abbreviations,
  being domain-specific when necessary, and ensuring names accurately reflect the
  function's behavior or data's purpose.
repository: twentyhq/twenty
label: Naming Conventions
language: TypeScript
comments_count: 9
repository_stars: 35477
---

Names should be descriptive and specific enough to clearly communicate their purpose and avoid confusion. This includes using full words instead of abbreviations, being domain-specific when necessary, and ensuring names accurately reflect the function's behavior or data's purpose.

Key guidelines:
- Use full words instead of abbreviations: `isRightToLeftLocale` instead of `isRtlLocale`
- Be domain-specific to avoid naming conflicts: `getSentFolderCandidatesByRegex` could be `getImapSentFolderCandidatesByRegex`
- Avoid ambiguous names that could cause confusion: `FlatEntityMapsCacheService` vs `WorkspaceFlatMapCacheService`
- Use descriptive variable names: `stepExecution.result` instead of `result.result`
- Be specific about scope and context: `useUpdateMultipleRecordsFromManyObjects` instead of `useUpdateManyRecordsFromManyObjects`

Example:
```typescript
// ❌ Ambiguous and abbreviated
const isRtlLocale = (locale: string) => { ... }
const mergeInProgressState = atom({ ... })

// ✅ Descriptive and specific  
const isRightToLeftLocale = (locale: string) => { ... }
const isMergeInProgress = atom({ ... })
```

This helps with IDE autocompletion, reduces naming conflicts, and makes code more self-documenting for better maintainability.