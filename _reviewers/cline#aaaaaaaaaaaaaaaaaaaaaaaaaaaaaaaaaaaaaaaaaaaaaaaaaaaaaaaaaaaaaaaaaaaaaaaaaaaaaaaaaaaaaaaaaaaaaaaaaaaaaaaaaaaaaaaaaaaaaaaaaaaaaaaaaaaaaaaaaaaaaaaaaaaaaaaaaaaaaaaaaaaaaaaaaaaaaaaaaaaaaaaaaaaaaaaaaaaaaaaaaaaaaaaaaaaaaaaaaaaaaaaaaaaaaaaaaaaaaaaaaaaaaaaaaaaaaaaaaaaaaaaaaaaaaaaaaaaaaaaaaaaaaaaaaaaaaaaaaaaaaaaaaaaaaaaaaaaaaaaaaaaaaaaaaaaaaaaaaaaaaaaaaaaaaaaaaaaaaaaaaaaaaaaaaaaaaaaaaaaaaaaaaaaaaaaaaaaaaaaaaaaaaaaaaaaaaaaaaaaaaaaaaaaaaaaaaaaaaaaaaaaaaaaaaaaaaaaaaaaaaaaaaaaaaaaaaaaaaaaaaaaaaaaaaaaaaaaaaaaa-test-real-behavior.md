---
title: Test real behavior
description: Tests should exercise real implementation and assert on user-observable
  outcomes rather than relying on shallow mocks or internal implementation details
  that can drift out of sync with the code. When a dependency's behavior is central
  to the bug or feature being tested (e.g., a Radix select's handling of re-selecting
  the same value), avoid replacing it with...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Testing
language: TSX
comments_count: 3
repository_stars: 70964
---

Tests should exercise real implementation and assert on user-observable outcomes rather than relying on shallow mocks or internal implementation details that can drift out of sync with the code. When a dependency's behavior is central to the bug or feature being tested (e.g., a Radix select's handling of re-selecting the same value), avoid replacing it with a simplified mock that masks the real logic—drive the actual component with user-event instead. Similarly, assert against what is actually rendered or returned (visible text, resolved state) rather than importing and reusing internal constants/helpers that may be renamed, removed, or diverge from the real UI. For async actions with success/failure paths (e.g., a commit that can be rejected), tests must verify the resulting state is correct for both outcomes—e.g., confirming that UI state (like a draft message) is only cleared when the operation actually succeeds, not merely that the action function was called.

Example of asserting on real, observable behavior instead of an internal helper:
```tsx
// Avoid:
expect(await screen.findByText(cloudAutoApproveTooltip("PyCharm"))).toBeInTheDocument()

// Prefer asserting the actual rendered text:
expect(await screen.findByText(/when PyCharm is closed\./)).toBeInTheDocument()
```