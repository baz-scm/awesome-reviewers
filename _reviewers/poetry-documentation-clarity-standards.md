---
title: Documentation clarity standards
description: Ensure documentation is grammatically correct, clearly structured, and
  uses precise terminology. Avoid verbose or repetitive explanations, and provide
  specific details that help users understand exactly what will happen.
repository: python-poetry/poetry
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 33496
---

Ensure documentation is grammatically correct, clearly structured, and uses precise terminology. Avoid verbose or repetitive explanations, and provide specific details that help users understand exactly what will happen.

Key practices:
- Use proper grammar and sentence structure ("The '.exe' extension... is placed" should be "The '.exe' extension is added to the file, and it is placed")
- Structure complex information with bullet points or lists for better readability
- Be precise with technical terms (specify "directory path dependencies" rather than just "path dependencies")
- Avoid unnecessarily verbose or repetitive phrasing
- When explaining technical concepts, provide intuitive explanations before detailed technical specifications

Example of improvement:
```
Before: "When set this configuration allows users to configure package distribution format policy for all or specific packages. Specifically, to disallow the use of binary distribution format for all, none or specific packages."

After: "When set, this configuration allows users to disallow the use of binary distribution format for all, none or specific packages."
```

This ensures documentation is accessible, accurate, and actionable for developers at all skill levels.