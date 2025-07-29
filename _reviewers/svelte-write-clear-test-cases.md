---
title: Write clear test cases
description: Tests should be written with clear intent and expectations. Use descriptive
  names that accurately reflect what the test validates, and include both positive
  and negative test cases to demonstrate expected behavior through contrast. Organize
  tests in appropriate suites based on their purpose (e.g., validation tests vs. runtime
  tests).
repository: sveltejs/svelte
label: Testing
language: Other
comments_count: 2
repository_stars: 83580
---

Tests should be written with clear intent and expectations. Use descriptive names that accurately reflect what the test validates, and include both positive and negative test cases to demonstrate expected behavior through contrast. Organize tests in appropriate suites based on their purpose (e.g., validation tests vs. runtime tests).

For example, when testing error conditions, include a passing case above the failing case:

```javascript
function validFunction() {
    return $state(1); // This should pass
}

function invalidFunction() {
    return $state(1); // This should throw, as expected
}
```

Avoid confusing names like importing something called "broken" when it's actually working correctly. Instead, use names that clearly indicate the test's purpose and expected outcome.