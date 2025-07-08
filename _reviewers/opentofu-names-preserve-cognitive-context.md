---
title: Names preserve cognitive context
description: Choose variable, function, and type names that preserve cognitive context
  by clearly indicating their purpose and relationship to surrounding code. Names
  should help readers understand the code's intent without having to deeply analyze
  implementation details.
repository: opentofu/opentofu
label: Naming Conventions
language: Go
comments_count: 3
repository_stars: 25901
---

Choose variable, function, and type names that preserve cognitive context by clearly indicating their purpose and relationship to surrounding code. Names should help readers understand the code's intent without having to deeply analyze implementation details.

Examples:
```go
// Poor naming - loses context
ctx := someFunc(refs)
psuedo := value.Decode()
targetedNodes := getExcludedItems()

// Good naming - preserves context
hclCtxFunc := someFunc(refs)  // Indicates it returns HCL context
decodedExpectedVar := value.Decode()  // Shows relationship to expected value
excludedNodes := getExcludedItems()  // Matches exclusion logic
```

This practice reduces cognitive load when reading code by:
1. Making the purpose of variables immediately clear
2. Maintaining consistency with surrounding context
3. Avoiding misleading names that could cause confusion
4. Helping readers predict behavior without checking implementation

When choosing names, consider:
- What does this value represent in the current context?
- How will it be used by surrounding code?
- What assumptions might readers make based on the name?