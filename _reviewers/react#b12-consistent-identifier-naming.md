---
title: Consistent Identifier Naming
description: 'Use naming that’s semantically accurate, consistent, and minimally noisy—especially
  when transforming/generated code.


  **Rules**

  1. **Don’t invent unnecessary identifier renames in destructuring.** Prefer shorthand
  when the local name matches the property key.'
repository: facebook/react#b12
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251896
---

Use naming that’s semantically accurate, consistent, and minimally noisy—especially when transforming/generated code.

**Rules**
1. **Don’t invent unnecessary identifier renames in destructuring.** Prefer shorthand when the local name matches the property key.
   - Good: `const { disabled } = t0;`
   - Avoid: `const { disabled: disabled } = t0;`
2. **Use the correct destructuring key form for non-identifier property names.** Quote keys that aren’t valid JS identifiers (e.g. dashed attributes).
   - `const { 'aria-label': ariaLabel } = t0;`
3. **Preserve explicit developer names.** Only apply synthetic naming for *anonymous* functions/constructs; if the original function was already named, don’t rename or wrap it with generated property-access indirections.
4. **Keep terminology consistent across APIs/tools; only suffix when semantics/data structures differ.** If you use “stack” for one concept, don’t rename it to “branch” just because the return shape changes—use a clear suffix instead (e.g., `react_get_owners_stack_trace` vs `react_get_owners_stack`).
5. **Minimize synthetic “noise” in generated identifiers.** Don’t add argument indices (like `arg0`) when it’s not adding meaningful disambiguation (e.g., special-cased React Effect hooks or when there’s only one anonymous argument).

**Example (property-key + shorthand)**
```js
const { disabled, 'aria-label': ariaLabel } = propsOrT0;
```