---
title: Name callbacks passed to hooks
description: When passing callback functions to React hooks (useEffect, useCallback,
  custom hooks, etc.), prefer giving them descriptive names instead of leaving them
  as inline anonymous functions, especially when a single hook call takes more than
  one function argument. Debugging and profiling tools (including the React Compiler's
  auto-naming pass) rely on call-site...
repository: facebook/react#b20
label: React
language: Markdown
comments_count: 2
repository_stars: 251895
---

When passing callback functions to React hooks (useEffect, useCallback, custom hooks, etc.), prefer giving them descriptive names instead of leaving them as inline anonymous functions, especially when a single hook call takes more than one function argument. Debugging and profiling tools (including the React Compiler's auto-naming pass) rely on call-site context to generate readable names for anonymous functions, but they can only disambiguate multiple anonymous arguments in the same call by index (e.g. `Component[useEffect(arg0)]`), which is far less useful than a clear name like `Component[useEffect]` or `Component[onClick]`. For example, instead of:

```javascript
useEffect(() => {
  doSomething();
}, [dep]);
```

if the effect logic is complex or there are multiple callbacks in one call, extract and name the function:

```javascript
const handleEffect = () => {
  doSomething();
};
useEffect(handleEffect, [dep]);
```

This keeps generated stack traces, profiler output, and compiler-generated debug identifiers meaningful, and avoids ambiguous `argN` suffixes when multiple inline callbacks are passed to the same hook.</description>
</invoke>
