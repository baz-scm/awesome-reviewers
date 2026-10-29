---
title: Type definitions must mirror runtime API
description: Public type signatures (TypeScript definitions, interfaces, etc.) must
  accurately reflect the actual runtime behavior of the API, not an idealized or overly
  broad version of it. Before adding a property, method, or parameter to a shared
  interface, verify it genuinely exists/works at every point where that interface
  is used — don't let convenience leak...
repository: chalk/chalk#CANARY-1ebfbbf4
label: API
language: TypeScript
comments_count: 4
repository_stars: 23342
---

Public type signatures (TypeScript definitions, interfaces, etc.) must accurately reflect the actual runtime behavior of the API, not an idealized or overly broad version of it. Before adding a property, method, or parameter to a shared interface, verify it genuinely exists/works at every point where that interface is used — don't let convenience leak unsupported members onto chained or derived objects (e.g. don't put `supportsColor` on the base `Chalk` interface if it only exists on the top-level export and `chalk.red.supportsColor` isn't actually valid at runtime). Likewise, match optionality and coercion exactly: if a constructor doesn't require an options object at runtime, mark the parameter optional (`options?: ChalkOptions`); if a function internally coerces inputs (e.g. numbers to strings), the type should accept the broader input (`unknown[]` instead of `string[]`) rather than being artificially narrow. For fluent/chainable APIs, prefer `this` as the return type over naming the concrete interface, so subclasses and composed types continue to chain correctly:

```ts
interface Chalk {
	rgb(r: number, g: number, b: number): this; // not: Chalk
}
```

When runtime behavior and type definitions diverge, treat it as a bug to resolve explicitly — either adjust the implementation to match the intended contract or adjust the types to match reality, but never ship a definition that promises something the API doesn't deliver.