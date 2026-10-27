---
title: React validation test coverage
description: When changing React-specific static analysis/validation (hooks rules,
  React compiler validations, wrapper/component detection), update both the detection
  logic and the test suite in lockstep.
repository: facebook/react#b8
label: React
language: TypeScript
comments_count: 3
repository_stars: 251889
---

When changing React-specific static analysis/validation (hooks rules, React compiler validations, wrapper/component detection), update both the detection logic and the test suite in lockstep.

Apply these rules:
1. Cover both “valid” and “invalid” examples, especially boundary/edge patterns.
2. Define the intended scope of what should be detected (e.g., only direct calls in a useEffect body vs calls inside nested functions).
3. Prevent false positives by making matching precise (e.g., when checking `React.*`, confirm the member expression base is `React`, and avoid treating arbitrary PascalCase wrappers as components unless you intentionally accept that tradeoff).
4. If detection is configurable or tradeoff-based (e.g., wrapper acceptance), add tests that demonstrate the chosen behavior (including known problematic wrappers).

Example test intent (illustrative):
```js
// Should be accepted
const memoized1 = React.memo(() => { useHook(); });
const memoized2 = memo(function Component(props) { useHook(); return null; });

// Should be rejected (or explicitly accepted if you choose the “accept everything” strategy)
const Component = debounce(() => { useHook(); });
```

And for “inside useEffect” scope:
```js
useEffect(() => {
  function foo() { effectEvent(); } // should be caught if nested traversal is intended
  foo();
}, []);
```

Result: reviewers can quickly confirm correctness, expected scope, and the false-positive/false-negative tradeoff via tests, not just code changes.