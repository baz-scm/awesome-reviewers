---
title: Clarify testing documentation
description: Ensure that testing documentation, including changelogs, API docs, and
  guides, uses clear and precise language that doesn't confuse developers. Avoid ambiguous
  statements that might mislead users who already understand the concepts, use proper
  technical terminology, and provide concrete examples that reflect real-world usage
  patterns.
repository: cypress-io/cypress
label: Testing
language: Markdown
comments_count: 3
repository_stars: 48850
---

Ensure that testing documentation, including changelogs, API docs, and guides, uses clear and precise language that doesn't confuse developers. Avoid ambiguous statements that might mislead users who already understand the concepts, use proper technical terminology, and provide concrete examples that reflect real-world usage patterns.

For example, when documenting testing behavior changes:
- Instead of: "assertions are now fully retryable" (when they already were)
- Use: "assertions now retry consistently in all contexts, including when chained with DOM commands"

When writing testing guides:
- Recommend building wrapper components "that will be close to how your users will use this component"
- Provide specific examples of realistic test scenarios

Always verify technical terms are properly capitalized (e.g., "WebKit" not "Webkit") and that explanations help rather than confuse the intended audience.