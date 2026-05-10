---
title: YAML-first config schema
description: When adding or changing configurable behavior, define it in the correct
  config scope and expose it via YAML/frontmatter—don’t introduce new diagram-specific
  syntax/directives, and don’t place diagram-only options in global config.
repository: mermaid-js/mermaid
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 87952
---

When adding or changing configurable behavior, define it in the correct config scope and expose it via YAML/frontmatter—don’t introduce new diagram-specific syntax/directives, and don’t place diagram-only options in global config.

**Rules**
1. **Use the diagram’s config schema for diagram-specific options** (the main/global config should not receive diagram-only variables). Keep docs consistent with the generated schema.
2. **Model nested configuration as nested objects** (e.g., `elk.nodePlacement.strategy` is an object path). Avoid ambiguous/flat structures that don’t match the existing nesting patterns.
3. **Prefer YAML/frontmatter over new custom keywords or deprecated directives**. If a feature needs configuration, make it a YAML `config:` entry.

**Examples**
- Replace deprecated directive with YAML frontmatter:
```markdown
---
config:
  markdownAutoWrap: false
---
```
- Move Gantt “working hours” from new syntax into YAML config:
```markdown
---
title: A Gantt Diagram
config:
  gantt:
    dateFormat: YYYY-MM-DD
    workdayStartTime: 08:00
    workdayEndTime: 17:00
---

gantt
  %% gantt content ...
```

Apply these rules for each new option so it has a single source of truth (schema), a clear location (scope), and a consistent user-facing configuration mechanism (YAML).