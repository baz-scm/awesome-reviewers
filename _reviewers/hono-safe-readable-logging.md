---
title: Safe, readable logging
description: 'When adding or modifying log output, keep messages concise, human-readable,
  and resistant to abuse:


  1. Format values for readability instead of raw numbers/bytes. For example, colorize
  HTTP status codes only when color output is enabled, and render sizes in human units
  (e.g. `746b`, `1.9kb`) rather than raw byte counts:'
repository: honojs/hono
label: Logging
language: TypeScript
comments_count: 4
repository_stars: 32741
---

When adding or modifying log output, keep messages concise, human-readable, and resistant to abuse:

1. Format values for readability instead of raw numbers/bytes. For example, colorize HTTP status codes only when color output is enabled, and render sizes in human units (e.g. `746b`, `1.9kb`) rather than raw byte counts:
```
<-- GET /
--> GET / 200 835ms 746b
<-- GET /
--> GET / 200 960ms 1.9kb
```

2. Never log unbounded or attacker-controlled data as-is. Request paths or query strings can be arbitrarily long and are attacker-controlled; logging them verbatim can flood stdout or degrade performance. Prefer truncating long paths/query strings (e.g. `/too/longgggggg...`) or capping the logged portion.

3. Avoid noisy, repetitive warnings for expected fallback behavior. A `console.warn` that fires on every request (e.g. when falling back from `performance.now()` to `Date.now()`) overwhelms the log output and provides no real value after the first occurrence. Compute such fallbacks once (e.g. via a module-level `??` expression) and warn a single time, rather than inside a per-request hot path.

Applying these practices keeps logs useful for debugging while avoiding performance regressions, log spam, or exposure to log-based denial-of-service via unbounded input.</description>
