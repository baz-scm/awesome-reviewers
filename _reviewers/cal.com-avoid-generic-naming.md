---
title: Avoid generic naming
description: Choose specific, descriptive names over generic ones for all identifiers
  including variables, functions, components, and test IDs. Generic names lack context
  and can cause confusion as the codebase grows. Names should clearly communicate
  their purpose and scope.
repository: calcom/cal.com
label: Naming Conventions
language: TSX
comments_count: 4
repository_stars: 37732
---

Choose specific, descriptive names over generic ones for all identifiers including variables, functions, components, and test IDs. Generic names lack context and can cause confusion as the codebase grows. Names should clearly communicate their purpose and scope.

Examples of improvements:
- `reference_id` → `trace_reference_id` (adds context about what type of reference)
- `ai` → `aiPhone` or `calAiPhone` (specifies the AI functionality)  
- `404-page` → `app-router-not-found-page` (indicates the specific context)
- `DeleteHistoryDialog` → `DeleteBookingDialog` (clarifies what is being deleted)

When naming identifiers, ask yourself: "Will another developer understand the purpose and scope of this identifier without additional context?" If not, make the name more specific and descriptive.