---
title: Consistent documentation formatting
description: 'Maintain consistent style in documentation files to improve readability
  and professionalism. Specifically:


  1. **Command references**: Use a consistent format when referring to CLI commands.
  Prefer either:'
repository: hashicorp/terraform
label: Code Style
language: Other
comments_count: 4
repository_stars: 45532
---

Maintain consistent style in documentation files to improve readability and professionalism. Specifically:

1. **Command references**: Use a consistent format when referring to CLI commands. Prefer either:
   - The explicit format: "The `terraform fmt` command" (includes both "The" and "command")
   - The concise format: "`terraform fmt`:" followed by a description

2. **Punctuation in lists**: Follow consistent punctuation rules in bullet lists:
   - Omit periods from incomplete sentences or phrases in bullet lists
   - Include periods only for complete sentences

**Example**:
```markdown
# Recommended

- `backend.tf`: Your backend configuration
- `main.tf`: Resource and data source blocks
- `variables.tf`: Variable blocks in alphabetical order

# Instead of

- `backend.tf`: Your backend configuration.
- `main.tf`: Resource and data source blocks.
- `variables.tf`: Variable blocks in alphabetical order.
```

Consistent documentation formatting ensures that users can quickly scan and comprehend content, while maintaining a professional appearance throughout the codebase.