---
title: Consistent Markdown Tables
description: When adding or editing tables in documentation, ensure the Markdown table
  is both syntactically continuous (so rows actually belong to the table) and stylististically
  consistent with existing docs.
repository: ossu/computer-science
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 203692
---

When adding or editing tables in documentation, ensure the Markdown table is both syntactically continuous (so rows actually belong to the table) and stylististically consistent with existing docs.

Apply these rules:
- Don’t insert extra/blank lines between the table header, separator row, and the data rows; a stray line can cause later entries to render outside the table.
- Match the existing column order and header/alignment pattern used in the surrounding documentation.
- Use the same header + separator format across related files.

Example (use the same structure/pattern as the surrounding docs):
```md
Courses | Duration | Effort
:-- | :--: | :--:
[Machine Learning by Andrew Ng](https://www.coursera.org/learn/machine-learning) | - | -
```
If a row appears missing in the rendered preview, first check for stray/extra lines that break the table block, then verify the header/separator pattern matches the established one.