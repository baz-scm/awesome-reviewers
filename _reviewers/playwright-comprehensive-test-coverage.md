---
title: comprehensive test coverage
description: Tests should be comprehensive and cover edge cases, complete scenarios,
  and use specific assertions rather than generic checks. When writing tests, include
  multiple test cases that validate different states, use precise count assertions
  instead of simple visibility checks, and ensure all relevant interactions are tested.
repository: microsoft/playwright
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 76113
---

Tests should be comprehensive and cover edge cases, complete scenarios, and use specific assertions rather than generic checks. When writing tests, include multiple test cases that validate different states, use precise count assertions instead of simple visibility checks, and ensure all relevant interactions are tested.

For example, instead of just checking visibility:
```ts
// Weak test
await expect(codeSnippets.first()).toBeVisible();

// Better test with specific counts
await expect(codeSnippets).toHaveCount(3);
await toggleCheckbox.click();
await expect(codeSnippets).toHaveCount(0);
```

When testing complex scenarios, include comprehensive cases:
```ts
// Simple test
await page.setContent(`<div inert><button>Second</button></div>`);

// More comprehensive test
await page.setContent(`
  <div aria-hidden="true"><button>First</button></div>
  <div inert><button>Second</button></div>
  <button>Third</button> <!-- not hidden for comparison -->
`);
await expect(page.getByRole('button')).toHaveCount(1); // only Third is visible
```

Always test edge cases like whitespace handling, empty states, and boundary conditions. Include tests for all relevant UI interactions such as expansion/collapse, toggling, and state changes.