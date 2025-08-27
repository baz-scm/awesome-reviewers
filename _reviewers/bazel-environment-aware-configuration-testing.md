---
title: Environment-aware configuration testing
description: When writing tests for configuration-dependent functionality, implement
  environment detection and conditional logic to handle platform-specific differences.
  Tests should detect system capabilities and adjust expectations accordingly rather
  than assuming uniform behavior across all environments.
repository: bazelbuild/bazel
label: Configurations
language: Shell
comments_count: 3
repository_stars: 24489
---

When writing tests for configuration-dependent functionality, implement environment detection and conditional logic to handle platform-specific differences. Tests should detect system capabilities and adjust expectations accordingly rather than assuming uniform behavior across all environments.

Key practices:
- Use capability detection before testing features that may not be universally supported
- Implement platform-specific path handling and formatting
- Adjust test expectations based on detected environment characteristics

Example from cross-platform path handling:
```bash
if is_windows; then
  expected_path=$(echo "$bazelrc" | sed 's/^C:/c:/; s/\//\\\\/g')
else
  expected_path="$bazelrc"
fi
expect_log "source: \"$expected_path\""
```

Example from compiler feature detection:
```bash
# Check if __builtin_FILE is supported and skip test if not supported
if ! compiler_supports_builtin_file; then
  echo "Skipping test: __builtin_FILE not supported"
  return
fi
```

This approach ensures tests are robust across different execution environments while maintaining meaningful validation of configuration behavior.