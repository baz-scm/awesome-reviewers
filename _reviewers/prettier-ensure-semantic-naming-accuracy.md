---
title: Ensure semantic naming accuracy
description: Names should accurately reflect the actual behavior, constraints, and
  purpose of the code element they represent. Misleading names create confusion and
  make code harder to understand and maintain.
repository: prettier/prettier
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 50772
---

Names should accurately reflect the actual behavior, constraints, and purpose of the code element they represent. Misleading names create confusion and make code harder to understand and maintain.

**Key principles:**
- Interface names should match their property requirements (e.g., avoid naming an interface `RequiredOptions` if it contains optional properties)
- Type names should clearly communicate their actual constraints and behavior
- Method and property names should consistently reflect their access patterns

**Example of problematic naming:**
```typescript
// Misleading - contains optional properties despite "Required" in name
export interface RequiredOptions {
  singleAttributePerLine: boolean;
  jsxBracketSameLine?: boolean; // Optional property in "Required" interface
}
```

**Better approach:**
```typescript
// Clear and accurate naming
export interface FormattingOptions {
  singleAttributePerLine: boolean;
  jsxBracketSameLine?: boolean;
}

// Or separate required vs optional
export interface RequiredFormattingOptions {
  singleAttributePerLine: boolean;
}
export interface OptionalFormattingOptions {
  jsxBracketSameLine?: boolean;
}
```

When reviewing code, ask: "Does this name accurately describe what this element actually does or contains?" Names that contradict their implementation create technical debt and developer confusion.