---
title: React Rule Detection
description: 'When changing React-specific static analysis/validation (Hooks rules,
  effect/state rules, wrapper detection), make the update *precise and test-backed*:
  add both valid and invalid examples, ensure the detection covers realistic invocation
  shapes (including nested/indirect calls), and avoid broad heuristics that create
  false positives.'
repository: facebook/react#b11
label: React
language: TypeScript
comments_count: 2
repository_stars: 251894
---

When changing React-specific static analysis/validation (Hooks rules, effect/state rules, wrapper detection), make the update *precise and test-backed*: add both valid and invalid examples, ensure the detection covers realistic invocation shapes (including nested/indirect calls), and avoid broad heuristics that create false positives.

Apply this standard as follows:

1. Add regression tests for both sides
- Include examples that should pass (e.g., `React.memo(() => { /* hooks */ })`, `memo(function (props) { /* hooks */ })`).
- Include examples that should fail (e.g., cases where a wrapper is not actually a component wrapper).

2. Cover indirect/nested invocation paths
- Don’t only detect the simplest/top-level call form. If a rule should block `setState`-like behavior in effects, also consider code where the relevant call is triggered from a nested function.

3. Prevent false positives from broad heuristics
- If your logic treats “PascalCase assigned to a wrapper call” as a component, constrain it: accept only known component wrappers (e.g., `memo`, `forwardRef`) or require an explicit allowlist (`componentWrappers`) rather than implicitly accepting arbitrary wrappers like `debounce`/`throttle`.

Example test intent (conceptual):
```js
// should be valid (known component wrapper)
const memoized1 = React.memo(() => {
  useHook();
});

const memoized2 = memo(function Component(props) {
  useHook();
  return null;
});

// should be invalid or not treated as a component wrapper (unknown wrapper)
const debounced = debounce(() => {
  useHook();
});

// should be flagged if the rule is meant to catch indirect invocation
const effectEvent = useEffectEvent(() => setState(true));
useEffect(() => {
  function foo() {
    effectEvent();
  }
  foo();
}, []);
```

This keeps React rule behavior predictable for developers: fewer surprising allowances, fewer missed violations, and faster confidence via targeted regression tests.