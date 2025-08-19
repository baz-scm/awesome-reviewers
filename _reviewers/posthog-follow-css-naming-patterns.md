---
title: Follow CSS naming patterns
description: Maintain consistency with established CSS naming conventions already
  used in the codebase. For CSS classes, follow BEM methodology when that's the existing
  pattern. For custom properties, use semantic names that clearly indicate their purpose
  and work across themes.
repository: PostHog/posthog
label: Naming Conventions
language: Css
comments_count: 2
repository_stars: 28460
---

Maintain consistency with established CSS naming conventions already used in the codebase. For CSS classes, follow BEM methodology when that's the existing pattern. For custom properties, use semantic names that clearly indicate their purpose and work across themes.

Examples:
- Use BEM-style class names: `&.FunnelBarHorizontal--has-optional-steps` instead of `&.has-optional-steps`
- Use semantic CSS custom properties: `--gray-1`, `--gray-2` for theme-agnostic color variables that automatically adapt to light/dark themes

This ensures code maintainability and helps other developers quickly understand the naming system in use.