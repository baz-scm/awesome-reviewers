---
title: Safe, configurable logging
description: 'Logging code—whether in middleware or reusable helpers—should be predictable,
  non-intrusive, and easy to format or disable.


  1. Don''t hardcode log statements inside library or helper functions that callers
  can''t control. Instead, return a result and let the caller decide what/if to log:'
repository: honojs/Hono
label: Logging
language: TypeScript
comments_count: 5
repository_stars: 32741
---

Logging code—whether in middleware or reusable helpers—should be predictable, non-intrusive, and easy to format or disable.

1. Don't hardcode log statements inside library or helper functions that callers can't control. Instead, return a result and let the caller decide what/if to log:
```ts
const result = await toSSG(app, fs)
if (result.success) {
  console.log('Static site generation completed!')
} else {
  console.log('Failed!', result.error?.message)
}
```

2. Avoid noisy or repeated log output. A warning that fires on every request (e.g. a fallback notice inside a hot path) quickly becomes log spam. Prefer emitting such warnings once, at initialization, rather than per-call:
```ts
const getTime: () => number =
  performance?.now?.bind(performance) ??
  (console.warn('performance.now is not supported, using Date.now'), Date.now.bind(Date))
```

3. Be careful about what you log from user-controlled input. Full request paths/query strings can be arbitrarily large or crafted to pollute logs or degrade performance; consider truncating or limiting what gets logged rather than dumping raw, unbounded strings.

4. Format log output for readability and keep formatting concerns isolated from the data. Color codes, byte sizes, etc. should be converted into human-friendly representations (e.g., render content length as `746b` or `1.9kb`) and color should be an explicit, opt-in formatting step rather than baked into the value itself.

Following these practices keeps logs useful, prevents performance/security issues from unbounded or repeated output, and gives consumers control over how and what gets logged.