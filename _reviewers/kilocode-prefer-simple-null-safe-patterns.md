---
title: prefer simple null-safe patterns
description: Use straightforward null-safe patterns instead of complex undefined/empty
  distinctions. Avoid `any` types that can hide potential null/undefined issues at
  runtime.
repository: kilo-org/kilocode
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 7302
---

Use straightforward null-safe patterns instead of complex undefined/empty distinctions. Avoid `any` types that can hide potential null/undefined issues at runtime.

When handling optional values, prefer simple fallback patterns like `|| {}` over complex checks that distinguish between undefined and empty objects. As noted in code reviews, "it's tricky to depend on a distinction between undefined and empty" because developers often add `|| {}` everywhere, making the distinction unreliable.

Example of preferred approach:
```typescript
// Prefer this simple pattern
await updateGlobalState("customSupportPrompts", message.values || {})

// Over complex undefined/empty distinctions
if (Object.keys(message?.values ?? {}).length === 0) {
  // complex logic here
}
```

Also avoid `any` types that mask null safety:
```typescript
// Avoid
const deleteMessagesForResend = async (cline: any, originalMessageIndex: number) => {

// Prefer explicit typing
const deleteMessagesForResend = async (cline: ClineProvider, originalMessageIndex: number) => {
```