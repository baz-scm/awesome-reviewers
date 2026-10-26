---
title: Document API contracts
description: 'When publishing a function/snippet, explicitly define the API contract:
  (1) platform/runtime assumptions, (2) input shape and required types, (3) option
  defaults/behavior, and (4) output/return type consistency. Ensure examples and docs
  match the contract.'
repository: 30-seconds/30-seconds-of-code
label: API
language: Markdown
comments_count: 5
repository_stars: 129334
---

When publishing a function/snippet, explicitly define the API contract: (1) platform/runtime assumptions, (2) input shape and required types, (3) option defaults/behavior, and (4) output/return type consistency. Ensure examples and docs match the contract.

**Apply as a checklist**
- **Platform**: If behavior depends on environment (e.g., Node vs browser), either provide separate variants or clearly label the runtime and the specific underlying API.
- **Inputs**: Prefer clear, intentional signatures (avoid ambiguous varargs when two fixed inputs are expected). Enforce/require expected types at the API boundary.
- **Options/defaults**: If you accept an `opts` parameter, document required fields and defaults (e.g., what happens when omitted).
- **Return type**: Keep return types consistent across all cases (prefer `[]` over `-1` when your return is otherwise an array).
- **Examples/semantics**: Examples should demonstrate the exact data passed to callbacks/handlers and the precise behavior (e.g., correct DOM selector choice).

**Example: consistent return type**
```js
// Prefer: always return an array
const indexOfAll = (arr, val) => {
  const indices = [];
  arr.forEach((el, i) => {
    if (el === val) indices.push(i);
  });
  return indices; // [] when not found
};
```