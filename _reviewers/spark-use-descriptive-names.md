---
title: Use descriptive names
description: Choose names that clearly convey purpose and context rather than generic
  or vague terms. Names should be self-documenting and provide sufficient information
  for developers to understand their role without additional investigation.
repository: apache/spark
label: Naming Conventions
language: Java
comments_count: 3
repository_stars: 41554
---

Choose names that clearly convey purpose and context rather than generic or vague terms. Names should be self-documenting and provide sufficient information for developers to understand their role without additional investigation.

Avoid generic prefixes like "My" or overly broad terms without context. Instead, use specific, descriptive names that indicate the entity's purpose or functionality.

Examples of improvements:
- `MyByteArrayOutputStream` → `ExposedBufferByteArrayOutputStream` (describes the specific functionality)
- `Inner` → `InnerJoinType` (provides domain context)
- `mightContainEven` → `evenNumbersFoundCount` (clarifies what the variable represents)

When naming decisions might seem unusual or counterintuitive, document the rationale to help future maintainers understand the choice. This is especially important when maintaining compatibility with existing APIs or external libraries.