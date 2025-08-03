---
title: Choose clear semantic names
description: 'Names should clearly and accurately convey their purpose, behavior,
  and content. Follow these guidelines:


  1. Use positive boolean flags:

  ```typescript'
repository: continuedev/continue
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 27819
---

Names should clearly and accurately convey their purpose, behavior, and content. Follow these guidelines:

1. Use positive boolean flags:
```typescript
// Bad
const IGNORE_NEXT_EDIT = false;
if (!IGNORE_NEXT_EDIT) { ... }

// Good
const IS_NEXT_EDIT_ACTIVE = true;
if (IS_NEXT_EDIT_ACTIVE) { ... }
```

2. Method names should precisely reflect their behavior:
- Use verbs that accurately describe the action
- Include plurality when handling multiple items
- Avoid ambiguous terms like "set" when "add" or "update" are more accurate

```typescript
// Bad
setDecoration(editor: Editor, ranges: Range[]) // "set" implies replacement
userId(): string // doesn't indicate it's a check

// Good
addDecorations(editor: Editor, ranges: Range[]) // clearly shows augmenting
isSignedIn(): boolean // clearly shows purpose
```

3. Choose descriptive, declarative names for parameters and variables:
```typescript
// Bad
budget_tokens: number // unclear what the budget represents

// Good
tokenBudget: number // clearly indicates purpose
```

This standard helps maintain code clarity, reduces confusion, and makes intentions immediately clear to other developers.