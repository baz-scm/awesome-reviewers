---
title: Accurate, visibility-aware naming
description: "Choose identifier names that precisely and unambiguously describe what\
  \ the thing represents or does, including its scope and intended visibility. \n\n\
  - Reflect actual behavior: a name should match what the code does, not just an initial\
  \ assumption. For example, a hook described as \"pre_execution\" but actually used\
  \ to run/execute a statement was renamed to..."
repository: python/cpython
label: Naming Conventions
language: Python
comments_count: 3
repository_stars: 77696
---

Choose identifier names that precisely and unambiguously describe what the thing represents or does, including its scope and intended visibility. 

- Reflect actual behavior: a name should match what the code does, not just an initial assumption. For example, a hook described as "pre_execution" but actually used to run/execute a statement was renamed to `statement_submitted_hook` because the original name misrepresented its timing/role. Before finalizing a name, check if it accurately matches the full behavior across all call sites.
- Signal visibility/intent: use a leading underscore (or otherwise clearly mark) members that are internal implementation details and not meant to be part of the public API, even if they are exposed via a property. E.g., a public `Process` property returning an internal callable should delegate to a method named `_process`, not `process`, to avoid implying it's public.
- Prefer descriptive, typed attributes over generic/opaque containers: instead of stashing multiple behaviors behind a single ambiguous field like a `flags` dict/string, expose them as explicitly named attributes (e.g., `rule.memo: bool`, `rule.fastpath: str | None`) so the purpose of each value is clear from its name and type alone.
- When a clear name conflicts with external constraints (e.g., avoiding words like "password" that trigger security scanners), document the reasoning in a comment near the declaration so the deviation from the obvious name is understood by future readers.

Applying these guidelines keeps identifiers self-explanatory, prevents misleading assumptions about behavior or access level, and reduces the need for readers to dig into implementation to understand intent.</description>
