---
title: Ensure comprehensive test coverage
description: When implementing new functionality or modifying existing code, always
  add corresponding tests that comprehensively cover the changes. This includes testing
  the main functionality, edge cases, error conditions, and different execution paths.
repository: bazelbuild/bazel
label: Testing
language: Java
comments_count: 9
repository_stars: 24489
---

When implementing new functionality or modifying existing code, always add corresponding tests that comprehensively cover the changes. This includes testing the main functionality, edge cases, error conditions, and different execution paths.

Key practices to follow:

1. **Add tests for new functionality**: Every new feature, method, or code path should have dedicated test coverage. As noted in one discussion: "The change affects the logic in RecursiveFileSystemTraversalFunction, I would still recommend adding a test case for that."

2. **Cover multiple scenarios**: Use parameterized tests or multiple test methods to cover different input combinations, configurations, and edge cases. Consider testing both positive and negative cases.

3. **Test different code paths**: When code has multiple execution branches (like different strategies or conditional logic), ensure each path is tested. For example: "Can you also parameterize these tests for `ctx.actions.write_file` and `ctx.actions.expand_template`?"

4. **Include edge cases and error conditions**: Don't just test the happy path. Test boundary conditions, invalid inputs, and error scenarios. As suggested: "Some more ideas for test cases: A regex with an alternation matching two different test strings, test strings containing metacharacters..."

5. **Verify transformations explicitly**: When testing data transformations or conversions, test both the input and output explicitly to ensure both halves of the operation work correctly.

Example of comprehensive test coverage:
```java
@Test
public void build_changedSourceDirectory_rebuildsTarget(@TestParameter Change change) {
  // Setup initial state
  setupInitialBuild();
  
  // Apply the change
  change.apply(getWorkspace().getRelative("pkg/dir"));
  
  // Verify the expected behavior
  buildTarget("//foo:a");
  assertContainsEvent(events.collector(), "Executing genrule //pkg:a");
}
```

This approach ensures that code changes are properly validated and reduces the risk of regressions in production.