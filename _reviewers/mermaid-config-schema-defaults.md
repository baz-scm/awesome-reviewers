---
title: Config schema defaults
description: 'When updating configuration schemas, ensure each config option is fully
  specified and not redundantly redefined.


  Apply these rules:

  1) **Always set `type` and `default` for new properties** so downstream consumers
  get predictable behavior and the schema remains type-correct.'
repository: mermaid-js/mermaid
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 87952
---

When updating configuration schemas, ensure each config option is fully specified and not redundantly redefined.

Apply these rules:
1) **Always set `type` and `default` for new properties** so downstream consumers get predictable behavior and the schema remains type-correct.
2) **Use inheritance from base config definitions** (`$defs` / `allOf`) and **remove redundant properties** that are already provided by the base schema—only override when behavior truly differs.
3) **Keep `default` consistent with the declared `type`** and (when you’re standardizing UX) align defaults across related diagram configs.

Example (pattern):
```yaml
properties:
  markdownAutoWrap:
    type: boolean
    default: true

BlockDiagramConfig:
  title: Block Diagram Config
  allOf: [{ $ref: '#/$defs/BaseDiagramConfig' }]
  description: The object containing configurations specific for block diagrams.
  type: object
  unevaluatedProperties: false
  properties:
    padding:
      type: number
      default: 8
# Note: don’t re-declare useMaxWidth here if BaseDiagramConfig already defines it with the desired default.
```
