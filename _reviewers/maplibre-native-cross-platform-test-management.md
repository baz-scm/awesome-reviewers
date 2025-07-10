---
title: Cross-platform test management
description: 'When working with tests that run across multiple platforms (iOS, Android,
  etc.), ensure proper configuration and handling of platform-specific issues:'
repository: maplibre/maplibre-native
label: Testing
language: Json
comments_count: 2
repository_stars: 1411
---

When working with tests that run across multiple platforms (iOS, Android, etc.), ensure proper configuration and handling of platform-specific issues:

1. Place test files in all relevant platform-specific directories to ensure they're properly recognized:
```
metrics/linux-gcc8-release/render-tests/...
ios-render-test-runner/...
android-render-test-runner/...
```

2. When excluding a test that fails on specific platforms:
   - Document the reason for exclusion with a clear comment or issue link
   - Specify the exclusion only for affected platforms when possible
   - Create a follow-up issue to investigate and fix the root cause

3. For inconsistent test results that vary by device or environment:
   - Document the specific conditions where failures occur
   - Consider conditional test execution rather than complete exclusion

This approach maintains test coverage across platforms while providing clear documentation for temporarily disabled tests.