---
title: React rule compliance
description: Code should be structured to match React’s static rules for hooks/components
  and effect side effects—both to avoid false positives and to ensure real violations
  are caught.
repository: facebook/react#b9
label: React
language: TypeScript
comments_count: 2
repository_stars: 251891
---

Code should be structured to match React’s static rules for hooks/components and effect side effects—both to avoid false positives and to ensure real violations are caught.

Apply this as follows:

1) Be explicit with wrapper patterns around hook-using functions
- Prefer known React wrappers (e.g., `React.memo`, `memo`) and ensure your component identifiers follow the expectations of the tooling (commonly PascalCase).
- Avoid using arbitrary wrappers (e.g., `debounce`, `throttle`, `observer`) as if they were component wrappers unless your linting/configuration is explicitly set up to recognize them.

Example (allowed patterns):
```ts
const Memoized = React.memo(() => {
  useSomeHook();
  return null;
});

const Memoized2 = memo(function Component(props: { ok: boolean }) {
  useSomeHook();
  return null;
});
```

2) Don’t trigger state updates from within `useEffect` execution paths
- Do not call `setState` (directly or via an `useEffectEvent` indirection) as part of logic that runs during `useEffect`.
- If you use `useEffectEvent`, assume that state updates it causes may be detected even when invoked indirectly.

Example (disallowed pattern):
```ts
const [state, setState] = useState(0);
const effectEvent = useEffectEvent(() => {
  setState(1);
});

useEffect(() => {
  effectEvent(); // should be treated as a violation if your lint/rules enforce no setState in effects
}, []);
```

3) Ensure test coverage mirrors real usage (especially for edge cases)
- When adding/updating React rule logic or configuring it, include both:
  - valid examples your codebase uses (so they remain allowed), and
  - ambiguous cases that could otherwise slip through or be misclassified.
- Add cases for wrapper/event indirection so the rule behavior is stable and predictable.