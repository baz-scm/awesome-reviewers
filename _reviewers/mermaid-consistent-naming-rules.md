---
title: Consistent Naming Rules
description: 'Adopt consistent, explicit identifier naming across diagrams and TypeScript
  APIs.


  **Rules**

  1) **Diagram ids/syntax keywords**

  - Use **lower-case** diagram identifiers.'
repository: mermaid-js/mermaid
label: Naming Conventions
language: TypeScript
comments_count: 10
repository_stars: 87952
---

Adopt consistent, explicit identifier naming across diagrams and TypeScript APIs.

**Rules**
1) **Diagram ids/syntax keywords**
- Use **lower-case** diagram identifiers.
- For **new/unstable syntax**, append **`-beta`** to the syntax/keyword the parser accepts.
- Keep semantic parts of names **uniform** (don’t introduce ad-hoc prefixes like `Mini` or extra suffixes like `Language` unless the codebase has a single established pattern).

2) **TypeScript naming style**
- **Types**: use **UpperCamelCase** (e.g., `DiagramStylesProvider`).
- **Interfaces**: prefer `interface` for object shapes when possible.

3) **Type-only files**
- Avoid using `.d.ts` for internal project types.
- Use a dedicated convention like **`.type.ts`** (e.g., `gantt.type.ts`).

4) **Exported fields/props**
- Prefer **explicit names** for public types (e.g., `width`/`height` over `w`/`h`) to improve readability for downstream users.

5) **Stability/compatibility for naming formats**
- If an identifier format is consumed externally (e.g., edge id strings), treat it as a contract: don’t rename/separator-change without an explicit compatibility plan.

**Example**
```ts
// diagram detector keyword
const detector: DiagramDetector = (txt) => /^\s*contextMap-beta/.test(txt);

// stable diagram config key naming: one established pattern
export interface MermaidConfig {
  contextMap?: MiniContextMapLanguageDiagramConfig; // avoid “Mini…Language…” unless consistent everywhere
}

// type-only file convention
// packages/mermaid/src/diagrams/gantt/gantt.type.ts
export type DiagramStylesProvider = (options?: Record<string, unknown>) => string;

// explicit fields
export interface NodeMetaData {
  width?: string;
  height?: string;
}
```