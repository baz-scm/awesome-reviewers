---
title: Test React Validation Rules
description: 'When updating React lint/compiler rules (hooks/components/effects),
  treat the change like a contract: add tests that cover both intended valid patterns
  and the most likely real-world/edge-case shapes.'
repository: facebook/react#b4
label: React
language: TypeScript
comments_count: 2
repository_stars: 251885
---

When updating React lint/compiler rules (hooks/components/effects), treat the change like a contract: add tests that cover both intended valid patterns and the most likely real-world/edge-case shapes.

**What to test**
- **Valid wrapper forms**: e.g., `React.memo(() => { useHook(); })` and `memo(function Component(){ useHook(); })`.
- **Heuristic false positives** (if detection is based on naming/wrapper shape): e.g., `const Component = debounce(() => { useHook(); });` should be rejected or explicitly covered as an accepted limitation.
- **Indirection inside `useEffect`**: calls that happen inside nested functions within the effect body (not just direct top-level calls), e.g.,
  ```ts
  const [state, setState] = useState(0)
  const effectEvent = useEffectEvent(() => { setState(true) })

  useEffect(() => {
    function foo() {
      effectEvent() // ensure your rule flags/permits this as intended
    }

    foo()
  }, [])
  ```

**Rule of thumb**
- If your detection relies on heuristics (like “PascalCase assigned from wrapper calls”), reduce surprises by either (a) restricting to known wrappers or allowing configuration, and/or (b) explicitly documenting and testing the known false-positive/false-negative behavior.

Applying this standard prevents regressions and makes rule behavior predictable for developers using common React patterns.