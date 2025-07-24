---
title: Consistent identifier naming
description: Follow consistent naming conventions for all identifiers to improve code
  quality, accessibility, and test reliability. Ensure correct spelling and adhere
  to established project patterns.
repository: n8n-io/n8n
label: Naming Conventions
language: Other
comments_count: 4
repository_stars: 122978
---

Follow consistent naming conventions for all identifiers to improve code quality, accessibility, and test reliability. Ensure correct spelling and adhere to established project patterns.

Key practices:
1. Use precise spelling in HTML attributes and test IDs
   ```javascript
   // ❌ Incorrect
   <label for="avalableInMCP">
   data-test-id="workflow-settings-vailable-in-mcp"
   
   // ✅ Correct
   <label for="availableInMCP">
   data-test-id="workflow-settings-available-in-mcp"
   ```

2. Establish and follow consistent casing conventions:
   - For Vue events: decide between camelCase (`thumbsUp`) or kebab-case (`thumbs-up`) and use consistently
   - For component props: follow project conventions for complex types

3. Use IDE tools and linters to enforce naming standards
   - Consider disabling overly restrictive rules team-wide rather than repeatedly suppressing them
   - Document naming conventions in your style guide for team alignment

This approach helps prevent broken references between HTML elements, ensures tests target the correct elements, and makes code more maintainable by following predictable patterns.