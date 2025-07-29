---
title: Justify configuration changes
description: When making configuration changes, especially dependency upgrades, provide
  clear justification for why the change is necessary rather than simply updating
  to the latest version. Explain the specific benefits, required features, or problems
  being solved.
repository: sveltejs/svelte
label: Configurations
language: Json
comments_count: 2
repository_stars: 83580
---

When making configuration changes, especially dependency upgrades, provide clear justification for why the change is necessary rather than simply updating to the latest version. Explain the specific benefits, required features, or problems being solved.

For dependency upgrades, identify the minimum version needed and the specific features that require the upgrade. Consider the impact on related tools and dependencies that may also need updating.

Example from a TypeScript upgrade discussion:
```json
// Instead of just upgrading to latest
"typescript": "^4.0.0"

// Provide justification in PR description:
// "TypeScript 3.7+ needed for optional chaining feature used in new code.
// Updated to 3.9.7 (minimum required) rather than 4.0.0 to minimize compatibility risks.
// Also updated sucrase dependency which requires compatible TypeScript version."
```

This approach helps reviewers understand the necessity of changes and prevents unnecessary upgrades that could introduce instability or compatibility issues.