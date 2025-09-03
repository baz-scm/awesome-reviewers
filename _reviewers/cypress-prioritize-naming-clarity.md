---
title: Prioritize naming clarity
description: Choose names and aliases that clearly communicate their purpose and meaning
  rather than optimizing for brevity or perceived elegance. Avoid abbreviated aliases
  that obscure the actual location or purpose of code elements, and resist adding
  premature complexity like numerical suffixes unless multiple variants actually exist.
repository: cypress-io/cypress
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 48850
---

Choose names and aliases that clearly communicate their purpose and meaning rather than optimizing for brevity or perceived elegance. Avoid abbreviated aliases that obscure the actual location or purpose of code elements, and resist adding premature complexity like numerical suffixes unless multiple variants actually exist.

For example, prefer explicit paths like `@packages/frontend-shared/src/gql-components` over cryptic aliases like `@cy/components` that require developers to mentally map the alias to its actual location. Similarly, use simple names like `ci` until you actually need `ci1` and `ci2` - don't add complexity in anticipation of future needs that may never materialize.

The goal is to make code self-documenting where a developer can understand what something is and where it comes from without needing to look up aliases or decipher naming conventions.