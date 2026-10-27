---
title: Comprehensive test coverage
description: Design tests and verification harnesses to cover the full scope of behavior
  rather than a narrow slice. When writing an assertion or check, generalize it to
  apply across all relevant outputs/configurations (e.g., every node in an AST, all
  backends/targets) instead of a single special case, so regressions elsewhere are
  caught too. When a change claims to fix...
repository: facebook/react#b20
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 251895
---

Design tests and verification harnesses to cover the full scope of behavior rather than a narrow slice. When writing an assertion or check, generalize it to apply across all relevant outputs/configurations (e.g., every node in an AST, all backends/targets) instead of a single special case, so regressions elsewhere are caught too. When a change claims to fix or preserve some behavior, add fixtures/regression tests for all known edge cases (including declarators, for-in/for-of loops, hoisted declarations, etc.); if some cases remain unhandled, explicitly add a failing/skipped fixture or file a tracked follow-up rather than leaving the gap silent. Additionally, keep tests robust against incidental changes: avoid brittle positional selectors (e.g., `page.locator('.monaco-editor').nth(1)`) that break when UI layout shifts, and instead use stable identifiers such as `data-testid` attributes (e.g., `'[data-testid="config-tab"] .monaco-editor'`) so tests reliably target the intended element across different app states (e.g., internals panel shown or hidden).