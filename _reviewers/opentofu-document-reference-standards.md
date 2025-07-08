---
title: Document reference standards
description: 'Maintain consistent and accurate reference practices throughout project
  documentation to enhance usability and maintainability. This includes:


  1. **Verify link accuracy**: Ensure all document cross-references point to the correct
  filenames and paths. Double-check file extensions and names before submitting changes.'
repository: opentofu/opentofu
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 25901
---

Maintain consistent and accurate reference practices throughout project documentation to enhance usability and maintainability. This includes:

1. **Verify link accuracy**: Ensure all document cross-references point to the correct filenames and paths. Double-check file extensions and names before submitting changes.

2. **Follow consistent linking conventions**: When referencing work in changelogs and release notes:
   - Link to issues for functional descriptions and design decisions
   - Link to PRs for technical implementation details
   - For larger features with multiple PRs, prefer linking to tracking issues

3. **Avoid redundancy**: Instead of duplicating information across multiple documentation files, reference a single source of truth:

```markdown
## Compatibility
For detailed compatibility information, see the [Migration Guide](https://example.org/docs/migration/).
```

Rather than:
```markdown
## Compatibility
- Version 1.6.2 is compatible with Tool X version 1.5.x
- Version 1.7.0 is compatible with Tool X version 1.6.x
```

Following these standards reduces maintenance burden and ensures that users can consistently find the most current and accurate information.