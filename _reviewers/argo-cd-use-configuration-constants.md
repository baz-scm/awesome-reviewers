---
title: Use configuration constants
description: Replace hardcoded values with named constants from common packages or
  make values configurable through environment variables or flags. This improves maintainability,
  reduces magic numbers, and enables runtime configuration.
repository: argoproj/argo-cd
label: Configurations
language: Go
comments_count: 5
repository_stars: 20149
---

Replace hardcoded values with named constants from common packages or make values configurable through environment variables or flags. This improves maintainability, reduces magic numbers, and enables runtime configuration.

Examples of good practices:
- Use `common.SyncOptionSkipDryRunOnMissingResource` instead of `"SkipDryRunOnMissingResource=true"`
- Make timeouts configurable: `dialTime := env.ParseDurationFromEnv("DIAL_TIMEOUT", 30*time.Second)`
- Use math.MaxInt instead of arbitrary limits like 100 for scalability
- Define constants for repeated values: `const defaultMaxChildren = 2`

Avoid hardcoding configuration values directly in the code. Instead, centralize them in common packages or make them configurable through environment variables, command-line flags, or configuration files. This allows for easier testing, deployment flexibility, and reduces the risk of inconsistencies across the codebase.