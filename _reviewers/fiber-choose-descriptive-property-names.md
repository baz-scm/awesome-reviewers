---
title: Choose descriptive property names
description: Property and configuration field names should clearly communicate their
  purpose, behavior, and relationships to other components. Avoid ambiguous or misleading
  names that require additional context to understand.
repository: gofiber/fiber
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 37560
---

Property and configuration field names should clearly communicate their purpose, behavior, and relationships to other components. Avoid ambiguous or misleading names that require additional context to understand.

When naming properties, consider:
- **Semantic accuracy**: Names should precisely reflect what the property represents or does
- **Behavioral clarity**: If a property has specific behavior (like fallback order), include that in the name
- **Consistency**: Follow established naming patterns within your codebase

Examples of improvements:
```go
// Poor: Ambiguous about whether it's for custom or predefined formats
CustomFormat string

// Better: Clear that it handles both predefined and custom formats
Format string

// Poor: Doesn't indicate these are fallback options
AdditionalKeyLookups []string

// Better: Clearly indicates fallback behavior and order
FallbackKeyLookups []string

// Poor: Inconsistent with standard naming patterns
IsLiveEndpoint string

// Better: Consistent with conventional endpoint naming
LivenessEndpoint string
```

Well-chosen names reduce cognitive load, improve code maintainability, and make APIs more intuitive for other developers to use.