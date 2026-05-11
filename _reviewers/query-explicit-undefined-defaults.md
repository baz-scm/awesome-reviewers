---
title: Explicit Undefined Defaults
description: 'Prevent `undefined`/`void`/falsy values from becoming accidental runtime
  states.


  Apply these rules:

  1. **Eliminate transient `undefined`**: If a value can be absent (e.g., localStorage,
  optional query data), wire an explicit `defaultValue` so hooks/state initialize
  to a concrete value and consumers never render an “undefined first frame”.'
repository: tanstack/query
label: Null Handling
language: TSX
comments_count: 5
repository_stars: 49380
---

Prevent `undefined`/`void`/falsy values from becoming accidental runtime states.

Apply these rules:
1. **Eliminate transient `undefined`**: If a value can be absent (e.g., localStorage, optional query data), wire an explicit `defaultValue` so hooks/state initialize to a concrete value and consumers never render an “undefined first frame”.
   - Prefer setting the `useState` initial value from `defaultValue` inside the utility hook rather than letting it be `undefined` and patching later.
2. **Guard globals by environment**: Never assume browser APIs exist—use a shared “is server/client” check before touching `window`/DOM.
3. **Treat `void`/no-arg and falsy as testable cases**: When designing/using optional variables or cached data, add type and runtime tests for `void` (no variables) and for falsy cached values (e.g., `''`, `0`, `false`) so “absent” isn’t conflated with “no result”.
4. **Don’t rely on `undefined` being “missing” during key/hash matching**: If keys are serialized/hashed (e.g., via `JSON.stringify`) or displayed via hashes, `undefined` may be removed, making different logical keys collide or fail to match.
   - Prefer key shapes where absence is explicit (e.g., use a dedicated sentinel or omit the property at the call site) and document/align hashing with comparison semantics.

Example (default to avoid initial `undefined`):
```ts
function useLocalStorage<T>(key: string, defaultValue: T) {
  const [value, setValue] = React.useState<T>(() => {
    const raw = localStorage.getItem(key)
    return raw == null ? defaultValue : (JSON.parse(raw) as T)
  })
  // ...sync back to localStorage
  return [value, setValue] as const
}
```

If a behavior constraint exists (e.g., a function must not return `undefined`), encode it in types and tests—don’t “test” impossible states.