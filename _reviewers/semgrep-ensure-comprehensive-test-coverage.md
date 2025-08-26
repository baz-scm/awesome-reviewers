---
title: Ensure comprehensive test coverage
description: Tests should validate all expected behaviors, variants, and edge cases
  rather than covering only the happy path. When implementing tests, ensure you include
  scenarios for all relevant configurations, types, or levels that your code supports.
repository: semgrep/semgrep
label: Testing
language: Yaml
comments_count: 3
repository_stars: 12598
---

Tests should validate all expected behaviors, variants, and edge cases rather than covering only the happy path. When implementing tests, ensure you include scenarios for all relevant configurations, types, or levels that your code supports.

Key practices:
- Test all variants of a feature (e.g., if testing severity levels, include tests for CRITICAL, HIGH, MEDIUM, LOW)
- Include proper test validation markers (e.g., `# ruleid: test-name` comments) to verify functionality
- Cover alternative implementations or types (e.g., if testing `string` type matching, also test `char*`)

Example from rule testing:
```yaml
# Instead of only testing one severity level:
rules:
- id: critical
  severity: CRITICAL

# Test multiple levels:
rules:
- id: critical-test
  severity: CRITICAL
- id: high-test  
  severity: HIGH
- id: medium-test
  severity: MEDIUM
```

This approach prevents silent failures when mappings or configurations change and ensures robust validation of your code's behavior across all supported scenarios.