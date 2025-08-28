---
title: Use descriptive names
description: Choose names that clearly communicate intent and purpose, avoiding vague
  or misleading terms. Names should be self-documenting and accurately reflect what
  the variable, function, or type represents.
repository: rocicorp/mono
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 2091
---

Choose names that clearly communicate intent and purpose, avoiding vague or misleading terms. Names should be self-documenting and accurately reflect what the variable, function, or type represents.

**Key principles:**
- Replace vague names with specific, descriptive alternatives
- Ensure function names accurately describe their behavior and return values
- Use descriptive parameter names that clarify their role
- Avoid generic terms when more specific ones are available

**Examples:**

```typescript
// ❌ Vague and misleading
function getView() { /* doesn't return anything useful */ }
const enabled: boolean; // too generic
const tableName = 'users'; // unclear if client or server name

// ✅ Clear and descriptive  
function useView() { /* name reflects side-effect behavior */ }
const isServerConnected: boolean; // specific about what's enabled
const serverTableName = 'users'; // clarifies which context

// ❌ Generic parameter names
function configure(name: string, args: unknown[]) { }

// ✅ Descriptive parameter names
function configure(--target-client-row-count: string, queryArgs: ReadonlyJSONValue[]) { }
```

This practice makes code self-documenting, reduces cognitive load for reviewers, and prevents misunderstandings about functionality. When names accurately reflect their purpose, the code becomes easier to maintain and debug.