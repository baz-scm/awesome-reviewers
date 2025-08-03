---
title: Use specific semantic names
description: Choose specific, descriptive names for identifiers that accurately reflect
  their purpose and behavior. Avoid generic terms or ambiguous names that could lead
  to confusion. Names should be self-documenting and convey precise meaning.
repository: microsoft/vscode
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 174887
---

Choose specific, descriptive names for identifiers that accurately reflect their purpose and behavior. Avoid generic terms or ambiguous names that could lead to confusion. Names should be self-documenting and convey precise meaning.

Key guidelines:
- Add clarifying prefixes/suffixes to distinguish similar concepts
- Avoid language keywords as identifiers
- Use names that reflect the exact functionality

Example - Improving name specificity:

```typescript
// ❌ Ambiguous or generic names
class AiRelatedInformation { }
function isPath(string: string) { }
interface SearchOptions { }

// ✅ Specific, semantic names
class AiSearchSettingKeysProvider { }
function isPathLike(text: string) { }
interface RipgrepTextSearchOptions { }
```

This helps prevent confusion, makes code more self-documenting, and reduces the need for additional clarifying comments.