---
title: Clear field documentation
description: Write precise, unambiguous documentation that explains what fields and
  methods represent rather than implementation details. Avoid recursive definitions,
  ambiguous terms, and focus on the user-facing behavior and purpose.
repository: kubernetes/kubernetes
label: Documentation
language: Go
comments_count: 7
repository_stars: 116489
---

Write precise, unambiguous documentation that explains what fields and methods represent rather than implementation details. Avoid recursive definitions, ambiguous terms, and focus on the user-facing behavior and purpose.

Key principles:
- Use precise terminology that accurately describes the field's purpose
- Explain what a field represents, not how it works internally  
- Avoid ambiguous words like "available" when "total" is more accurate
- Make documentation self-contained rather than recursive
- Be explicit about what operations do and don't do

Examples of improvements:

Instead of:
```go
// Value defines how much of a certain device capacity is available.
// If the capacity is consumable, the consumed amount is deducted and cached in memory by the scheduler.
```

Write:
```go
// Value defines the total amount of this capacity the device has.
// This field reflects the fixed total capacity and does not change.
```

Instead of:
```go
// container name
```

Write:
```go
// The name of the container requesting resources.
```

Instead of recursive definitions:
```go
// Mixins defines the mixins available for devices and counter sets
```

Write:
```go
// Mixins provides common definitions that can be used for devices and counter sets in the ResourceSlice.
```

This approach ensures documentation is immediately understandable without requiring knowledge of implementation details or other parts of the system.