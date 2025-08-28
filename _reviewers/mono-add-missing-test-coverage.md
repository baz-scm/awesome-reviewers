---
title: Add missing test coverage
description: Identify and address gaps in test coverage by requesting specific tests
  for untested functionality. When reviewing code changes, look for new features,
  complex logic, or critical interactions that lack corresponding tests. Focus on
  testing type inference, component interactions, edge cases, and different code paths.
repository: rocicorp/mono
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 2091
---

Identify and address gaps in test coverage by requesting specific tests for untested functionality. When reviewing code changes, look for new features, complex logic, or critical interactions that lack corresponding tests. Focus on testing type inference, component interactions, edge cases, and different code paths.

Examples of coverage gaps to watch for:
- Type inference validation: "Can you add a test that the inference works? Should not need to provide type on `id` in query func."
- Component interaction testing: "Would be good to add a basic test of the interaction with MutationTracker, probably using a mock."
- Missing test cases for new functionality: "Please add a test case for push with a compound partition key."
- Authentication and authorization logic: "we should really add tests for these"

When identifying coverage gaps, be specific about what needs testing and suggest appropriate testing approaches (unit tests, integration tests, mocking, etc.). Prioritize testing critical business logic, error handling, and complex interactions between components.