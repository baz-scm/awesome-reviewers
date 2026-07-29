---
title: Regex Guardrails for Filters
description: 'When implementing CLI output filters (regex/pattern matchers), make
  the match logic algorithmically safe: add explicit bypass guards for structured/machine-readable
  output and use precise patterns for command variants, then lock behavior with include/exclude
  regression tests.'
repository: diegosouzapw/OmniRoute
label: Algorithms
language: Json
comments_count: 3
repository_stars: 33162
---

When implementing CLI output filters (regex/pattern matchers), make the match logic algorithmically safe: add explicit bypass guards for structured/machine-readable output and use precise patterns for command variants, then lock behavior with include/exclude regression tests.

Apply this standard:
1) Add structured-output bypasses
- If a command supports JSON/YAML/template output, ensure the filter does nothing when those flags are present (e.g., by using negative lookahead like `(?!.*--json)` or `(?!.+-o\s+(?:json|yaml|jsonpath|go-template|template\/name)\b)` depending on your command style).

2) Use explicit alternation for CLI syntax variants
- Prefer patterns that directly encode known forms (e.g., `docker compose` vs `docker-compose`) rather than fuzzy modifiers that won’t match real whitespace-separated variants.

3) Test both inclusion and exclusion
- Add tests that assert:
  - the filter matches the intended “noise-stripping” commands, and
  - the filter does NOT match (or claims nothing) for structured-output invocations and for unrelated subcommands.

Example (pattern-bypass + explicit variants):
```js
const kubectlMatch = {
  outputTypes: ['kubectl'],
  commands: [
    // match kubectl actions
    '^kubectl\s+(?:get|describe|logs|apply|delete|rollout|exec|top|events?)\b',
    // bypass if structured output is requested (illustrative)
    '^(?!.*-o\s+(?:json|yaml|jsonpath|go-template)\b).*kubectl\s+(?:get|describe)\b'
  ]
};
```
(Shape the bypass to each CLI’s actual flags/outputs.)

This prevents corrupted structured data, reduces over-matching, and makes the filter’s behavior predictable over time.