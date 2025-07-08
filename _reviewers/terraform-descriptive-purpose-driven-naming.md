---
title: Descriptive purpose-driven naming
description: Choose identifiers that accurately describe their purpose and behavior,
  not just their type or how they're used. Names should be specific enough to understand
  their role without requiring additional context.
repository: hashicorp/terraform
label: Naming Conventions
language: Go
comments_count: 6
repository_stars: 45532
---

Choose identifiers that accurately describe their purpose and behavior, not just their type or how they're used. Names should be specific enough to understand their role without requiring additional context.

When naming methods, focus on what they actually do: 'AddAll' is more accurate than 'Merge' for a method that adds items from one set to another without creating a new set. For parameters and fields, use prefixes to clarify their scope or target: 'object_tags' is clearer than just 'tags' when specifically tagging an object.

For type or class names that represent specialized versions of concepts, use standard prefixes consistently (e.g., 'Abs' prefix for absolute references):

```go
// Good
type AbsActionInvocation struct {
    TriggeringResource AbsResourceInstance
    Action             AbsActionInstance
}

// Avoid
type ActionInvocation struct { 
    // Unclear whether these are absolute or relative references
}
```

For configuration attributes and flags, choose names that communicate their effect clearly:

```hcl
# Good: Clearly indicates when the override applies
override_during = "plan"

# Avoid: Vague about what is being affected
override_computed = true
```

Avoid variable names that are common English words ('said') or ambiguous acronyms. Instead use descriptive compound names ('storageAccountId') that precisely communicate intent.