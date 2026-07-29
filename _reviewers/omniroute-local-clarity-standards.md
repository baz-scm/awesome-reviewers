---
title: Local Clarity Standards
description: 'When updating code, optimize for local clarity and correctness, not
  “cleanup” by indirection.


  Apply these rules:

  1) Prefer locality over forced DRY

  - If a constant/abstraction is used once, keep it local. Don’t add module-scope
  indirection unless it materially improves maintainability.'
repository: diegosouzapw/OmniRoute
label: Code Style
language: TypeScript
comments_count: 9
repository_stars: 33162
---

When updating code, optimize for local clarity and correctness, not “cleanup” by indirection.

Apply these rules:
1) Prefer locality over forced DRY
- If a constant/abstraction is used once, keep it local. Don’t add module-scope indirection unless it materially improves maintainability.
- Keep configuration entries self-contained even if it duplicates an existing pattern; avoid helpers that create implicit coupling when different providers may evolve independently.

2) Improve readability with explicit intent
- Use clear derived booleans for control-flow (e.g., “passthrough” flags).
- Avoid mutation surprises: when a branch should be symmetric, assign the derived variable explicitly (e.g., `translatedBody = body`), rather than relying on implicit state.

3) Type-safety as a style baseline
- Let type guards do the work: remove redundant casts when `typeof`/guards already narrow.
- Avoid introducing `any` for new helpers; use focused interfaces and `Partial<...>` for recovery/state update parameters.

4) Preserve formatting in content transforms
- In response cleaning/translation paths, avoid broad whitespace normalization or tag stripping that can mangle markdown, code blocks, tables, or indentation. Only remove content you explicitly intend to remove.

Example (readability + type narrowing):
```ts
// Prefer guard-driven simplification over redundant casts
if (aliases && parsed.model) {
  const directTarget = aliases[parsed.model];
  if (typeof directTarget === "string" && directTarget.includes("/")) {
    const slashIdx = directTarget.indexOf("/');
    if (slashIdx !== -1) {
      const providerPart = directTarget.slice(0, slashIdx);
      const modelPart = directTarget.slice(slashIdx + 1);
      // ...
    }
  }
}
```

Example (format-preserving cleaning):
```ts
function cleanResponse(text: string, strip = true): string {
  let t = text;
  // Remove only known unwanted tags/markers
  t = t.replace(/<[?]xml[^?]*[?]>/g, "");
  // Intentionally DO NOT collapse spaces/newlines, to preserve markdown/code formatting
  return strip ? t.trim() : t;
}
```