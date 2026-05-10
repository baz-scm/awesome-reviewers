---
title: Options-Based API Design
description: 'When designing/typing internal and public APIs, keep signatures tight
  and future-proof:


  - Don’t pass parameters you don’t use. If `config` isn’t needed, remove it from
  the function signature (or make it optional only where truly required).'
repository: mermaid-js/mermaid
label: API
language: TypeScript
comments_count: 5
repository_stars: 87952
---

When designing/typing internal and public APIs, keep signatures tight and future-proof:

- Don’t pass parameters you don’t use. If `config` isn’t needed, remove it from the function signature (or make it optional only where truly required).
- Prefer a single options object over adding more positional parameters. This keeps the API extensible and avoids churn.
- Apply behavior consistently at the public entrypoint (e.g., preprocessing should happen inside the specific API users call, not only in constructors or other internal paths).
- Treat exported/internal types as contract surfaces: document changes and/or isolate unstable types behind dedicated entrypoints or explicit “internal/alpha” markings.

Example (extensible options object):

```ts
type ShapeOptions = {
  config?: { themeVariables: unknown };
};

export const filledCircle = (
  parent: SVG,
  node: Node,
  { config }: ShapeOptions = {}
) => {
  const themeVariables = config?.themeVariables;
  // ...render using themeVariables (or a default if absent)
};
```

Example (prefer optional/options instead of extra required positional params):

```ts
type RenderDraw = (
  text: string,
  id: string,
  version: string,
  diagramObject: Diagram,
  opts?: { error?: Error | null }
) => void;
```

Applying these standards reduces breaking changes, makes internal renderer/diagram code easier to evolve, and ensures public APIs behave predictably.