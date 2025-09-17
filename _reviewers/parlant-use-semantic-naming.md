---
title: Use semantic naming
description: Choose names that clearly communicate the purpose, behavior, or domain
  concept rather than generic or abbreviated terms. Names should be self-documenting
  and reflect what the entity actually does or represents.
repository: emcie-co/parlant
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 12205
---

Choose names that clearly communicate the purpose, behavior, or domain concept rather than generic or abbreviated terms. Names should be self-documenting and reflect what the entity actually does or represents.

Replace generic names with descriptive alternatives that convey meaning:
- `check` → `coherence_check` (specifies what type of check)
- `index` → `connection_proposition` (describes the actual concept)
- `evaluation_service` → `BehavioralChangeEvaluator` (clarifies the specific type of evaluation)

Maintain consistency in naming patterns across similar contexts. For example, if addressing an agent in test scenarios, consistently use second person ("when you do X") rather than mixing with third person ("when the agent does X").

This approach makes code more readable, reduces the need for additional documentation, and helps maintain consistency across the codebase by establishing clear semantic patterns.