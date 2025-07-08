---
title: Use precise semantic names
description: Choose names that accurately reflect the purpose and semantics of the
  entity being named. Avoid overloaded or ambiguous terms that could lead to confusion
  or misinterpretation.
repository: hashicorp/terraform
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 45532
---

Choose names that accurately reflect the purpose and semantics of the entity being named. Avoid overloaded or ambiguous terms that could lead to confusion or misinterpretation.

For example:
- Use specific names like `Result` instead of generic overloaded terms like `Resource` when the context requires precision
- In comments and documentation, ensure terminology is accurate (e.g., "list resource type name" rather than "managed resource type name" when referring to list resources)
- Use the proper established terminology in your domain (e.g., "type constraints" rather than "string" when referring to Terraform types)
- Follow consistent naming conventions by adhering to your team's style guide rather than creating ad-hoc naming rules

When creating a new name or choosing between alternatives, ask: "Will this name clearly communicate the entity's purpose to someone unfamiliar with this code?" If multiple teams or systems interact with your code, ensure your naming aligns with established patterns that all stakeholders understand.