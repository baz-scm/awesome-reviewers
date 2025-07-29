---
title: Runtime configurable defaults
description: Prefer runtime-configurable values over hardcoded constants to allow
  users to customize behavior without recompilation. Use environment variables with
  `os.getenv_opt()` for runtime configuration instead of compile-time constants with
  `$d()`, and consider environment variables instead of complex CLI parsing.
repository: vlang/v
label: Configurations
language: Other
comments_count: 5
repository_stars: 36582
---

Prefer runtime-configurable values over hardcoded constants to allow users to customize behavior without recompilation. Use environment variables with `os.getenv_opt()` for runtime configuration instead of compile-time constants with `$d()`, and consider environment variables instead of complex CLI parsing.

**Why this matters:**
- Runtime configuration allows users to adjust behavior without recompiling
- Environment variables provide a standard, cross-platform way to customize settings
- Reduces the need for complex command-line argument parsing
- Makes tools more flexible for different use cases and environments

**How to apply:**
```v
// Instead of hardcoded constants:
const indexexpr_cutoff = 10

// Use runtime-configurable defaults:
const indexexpr_cutoff = os.getenv_opt('VET_INDEXEXPR_CUTOFF') or { '10' }.int()

// For buffer sizes and similar values:
const buff_size = int($d('gg_text_buff_size', 2048))

// Instead of complex CLI parsing for tools:
// Use environment variables like VDIFF_TOOL, VTMP_DIR, etc.
```

This approach allows users to customize behavior with simple commands like `VET_INDEXEXPR_CUTOFF=99 v vet .` without requiring recompilation or complex flag combinations.