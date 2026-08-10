---
title: Prefer typed themed styles
description: 'Adopt maintainable UI code style rules:


  1) Avoid explicit `any` / lint ignores—use real types

  - Don’t rely on `any` and don’t silence type linting unless you provide a typed
  alternative.'
repository: supermemoryai/supermemory
label: Code Style
language: TSX
comments_count: 3
repository_stars: 28844
---

Adopt maintainable UI code style rules:

1) Avoid explicit `any` / lint ignores—use real types
- Don’t rely on `any` and don’t silence type linting unless you provide a typed alternative.
- Prefer narrowing, discriminated unions, or mapping SDK dynamic payloads to a safe internal type.

2) Don’t hardcode Tailwind arbitrary hex colors
- Replace `bg-[#1F2428]`-style arbitrary values with design-system/theme tokens (or extend Tailwind/theme) so colors are consistent and easy to update.

3) Keyboard handlers: make behavior explicit
- If you change how a key should behave (e.g., intercept Enter), call `e.preventDefault()` when the default action would otherwise occur, and keep the condition logic readable.

Example patterns:
```ts
// 1) Prefer typed/narrowed data over `any`
type AssistantMessagePart = { type: 'text'; text: string };

function extractTextPart(parts: unknown): string | null {
  if (!Array.isArray(parts)) return null;
  const part = parts.find(
    (p): p is AssistantMessagePart =>
      typeof p === 'object' && p !== null && (p as any).type === 'text'
  );
  return part?.text ?? null;
}

// 2) Theme token instead of arbitrary hex (example)
// Bad: className="bg-[#1F2428] ..."
// Good: className="bg-surface ..." (token defined in theme)

// 3) Keyboard handler with explicit default prevention
function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    // submit/send
  }
}
```

Use this as a default in UI components: typed data, tokenized styles, and explicit event behavior.