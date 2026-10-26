---
title: Conservative React Linting
description: 'When changing React hook/state linting or compiler validations, treat
  the detection logic as a contract: be conservative to avoid false positives, and
  lock behavior down with tests that include both valid and tricky invalid patterns.'
repository: facebook/react#b3
label: React
language: TypeScript
comments_count: 2
repository_stars: 251883
---

When changing React hook/state linting or compiler validations, treat the detection logic as a contract: be conservative to avoid false positives, and lock behavior down with tests that include both valid and tricky invalid patterns.

Apply this standard:
- Define supported patterns explicitly (e.g., “direct call inside `useEffect`” vs “call from nested function/recursive path”). If you only handle one, don’t silently broaden without tests.
- Use conservative component/hook inference. If you infer “component-ness” from wrappers, prefer hard-coding known wrappers (e.g., `memo`, `forwardRef`) or require a configurable allowlist of wrapper functions rather than accepting any wrapper call that happens to be assigned to a PascalCase variable.
- Add/expand tests every time detection heuristics change: include:
  - Valid examples that must pass.
  - Invalid examples that should fail (including past false-positive patterns).
  - Edge cases that clarify scope (direct vs indirect/nested calls).

Example (component wrapper false positives):
```ts
// Should be valid (known wrappers)
const Memoized = React.memo(() => { useHook(); });
const MemoFn = memo(function ComponentLike() { useHook(); });

// Should NOT be treated as safe just because it’s PascalCase
const Component = debounce(() => { useHook(); }); // ensure tests cover this
```

Example (useEffectEvent scope clarity):
```ts
const [state, setState] = useState(0);
const effectEvent = useEffectEvent(() => { setState(true); });

useEffect(() => {
  // If your rule only checks direct calls, test and document that behavior.
  effectEvent();

  function foo() {
    effectEvent();
  }
  foo(); // include a test to confirm whether indirect/nested paths are (or aren’t) detected
}, []);
```

Outcome: fewer silent acceptance of incorrect React patterns, clearer rule semantics, and safer refactors as the rules evolve.