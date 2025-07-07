---
title: Be explicit in references
description: When writing documentation, always be specific and explicit when referring
  to files, tools, configurations, or other elements. Vague references create confusion
  and require readers to make assumptions or search for additional context.
repository: tensorflow/tensorflow
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 190625
---

When writing documentation, always be specific and explicit when referring to files, tools, configurations, or other elements. Vague references create confusion and require readers to make assumptions or search for additional context.

Provide complete information by:

1. Specifying exact versions and names of tools mentioned
   Example: Use "Bazel 0.4.5" instead of just "0.4.5" in a table cell

2. Clearly stating file locations when referencing them
   Example: Write "env files in the envs/ folder" instead of just "env files"

3. Using descriptive headers that accurately reflect content
   Example: Use "Build tools" instead of "Bazel/Cmake" when the table shows various build tools

This practice ensures documentation is immediately clear to all readers, regardless of their familiarity with the codebase, and reduces the need for clarifying questions.