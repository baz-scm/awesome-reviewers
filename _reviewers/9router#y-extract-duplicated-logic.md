---
title: Extract duplicated logic
description: 'When the same logic appears in multiple places—across different files
  or in multiple branches of the same function—extract it into a single shared helper
  function or module instead of copy-pasting. Duplicated implementations tend to drift
  apart over time: a bug fix or behavior change applied to one copy is easily forgotten
  in the other(s), leading to...'
repository: decolua/9router#y
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31751
---

When the same logic appears in multiple places—across different files or in multiple branches of the same function—extract it into a single shared helper function or module instead of copy-pasting. Duplicated implementations tend to drift apart over time: a bug fix or behavior change applied to one copy is easily forgotten in the other(s), leading to inconsistent behavior.

Examples of this pattern to watch for:
- Two executors/translators implementing the same parsing, repair, or unwrap logic (e.g. token-refresh HTTP calls with identical headers and response unwrapping, or JSON-argument repair functions used by multiple translators) should be moved into a shared service/module and imported by both call sites.
- Multiple branches within the same function computing the same derived value (e.g. a "finish reason" computed independently in a flush path and a completion path) should be factored into a small named helper, such as `computeFinishReason(state)`, and called from each branch.

When extracting, give the shared function a clear name that describes its purpose, place it in a logical shared location (e.g. a `concerns/` or `services/` module), and add a brief comment if the logic relies on non-obvious state (such as sticky flags) so future readers understand why it behaves the way it does. This keeps the codebase DRY, reduces maintenance risk, and makes intent easier to follow.