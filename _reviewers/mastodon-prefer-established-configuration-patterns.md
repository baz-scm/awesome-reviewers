---
title: prefer established configuration patterns
description: When making configuration choices, prioritize existing centralized configuration
  values and established patterns over ad-hoc solutions or deprecated frameworks.
  This reduces technical debt and maintains consistency across the codebase.
repository: mastodon/mastodon
label: Configurations
language: TSX
comments_count: 2
repository_stars: 48691
---

When making configuration choices, prioritize existing centralized configuration values and established patterns over ad-hoc solutions or deprecated frameworks. This reduces technical debt and maintains consistency across the codebase.

Use centralized configuration exports instead of direct API calls:
```javascript
// Avoid direct browser API calls
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

// Prefer existing centralized configuration
import { reduceMotion } from 'mastodon/initial_state';
```

Similarly, avoid deprecated frameworks when the team is actively migrating away from them:
```javascript
// Avoid if migrating away from rails-ujs
Rails.delegate(/* ... */);

// Consider alternative approaches that align with migration plans
```

Before introducing new configuration approaches, check if equivalent centralized values or patterns already exist in the codebase. This ensures consistency and reduces maintenance overhead during framework migrations or refactoring efforts.