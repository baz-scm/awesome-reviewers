---
title: Semantically precise identifiers
description: Choose names for variables, fields, methods, and model identifiers that
  precisely and unambiguously reflect their actual behavior or content, especially
  when similar concepts could be confused (e.g., read vs. write costs, latest vs.
  specific version). Avoid encoding metadata into a name when it can instead be represented
  as a separate structured attribute...
repository: Helicone/helicone
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 6248
---

Choose names for variables, fields, methods, and model identifiers that precisely and unambiguously reflect their actual behavior or content, especially when similar concepts could be confused (e.g., read vs. write costs, latest vs. specific version). Avoid encoding metadata into a name when it can instead be represented as a separate structured attribute (e.g., don't bake quantization info like `fp8` into a model name if it's already tracked as an attribute elsewhere, such as in `endpoints.ts`). When a method's behavior has a specific nuance (e.g., it always returns the latest version), the name should make that explicit rather than leaving it generic.

Example:
```ts
// Avoid: ambiguous field name when multiple cost variants exist
interface CostBreakdown {
  cachedInputCost: number; // read cost? write cost? both?
}

// Prefer: explicit, unambiguous naming
interface CostBreakdown {
  cacheReadInputCost: number;
}

// Avoid: generic name hiding important behavior
public async getGatewayConfig(id: string) { ... } // actually returns latest version

// Prefer: name reflects actual behavior
public async getLatestGatewayConfig(id: string) { ... }
```

During review, flag names that are vague, redundant with existing structured data, or could be confused with a closely related concept, and propose a more descriptive alternative.</description>
