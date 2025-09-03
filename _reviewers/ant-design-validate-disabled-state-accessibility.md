---
title: validate disabled state accessibility
description: When UI components with interactive elements (like buttons with href
  attributes) are disabled, ensure they maintain proper accessibility standards and
  don't create security vulnerabilities. Disabled states should properly prevent user
  interaction while maintaining clear visual and programmatic indication of their
  state.
repository: ant-design/ant-design
label: Security
language: Markdown
comments_count: 1
repository_stars: 95882
---

When UI components with interactive elements (like buttons with href attributes) are disabled, ensure they maintain proper accessibility standards and don't create security vulnerabilities. Disabled states should properly prevent user interaction while maintaining clear visual and programmatic indication of their state.

Improperly handled disabled states can lead to security issues where users might interact with elements that should be non-functional, potentially bypassing intended security controls or creating confusing user experiences that could be exploited.

Example from the discussion:
```markdown
- 🐞 Fix accessibility issue when Button `href` is disabled.
```

Always verify that disabled interactive components:
- Properly prevent click/navigation events
- Maintain appropriate ARIA attributes
- Provide clear visual indication of disabled state
- Don't create accessibility barriers for screen readers