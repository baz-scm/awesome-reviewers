---
title: Follow established testing patterns
description: When writing tests, use existing patterns and infrastructure already
  established in the codebase rather than creating custom implementations. This improves
  consistency, reduces maintenance burden, and helps ensure comprehensive test coverage.
repository: aws/aws-sdk-js
label: Testing
language: Other
comments_count: 3
repository_stars: 7628
---

When writing tests, use existing patterns and infrastructure already established in the codebase rather than creating custom implementations. This improves consistency, reduces maintenance burden, and helps ensure comprehensive test coverage.

For feature tests:
- Identify common operations (like list/describe) that already have standard patterns
- Reuse existing step definitions when possible

For unit tests:
- Include tests for both positive and negative scenarios when features have toggles
- When implementation changes affect tests, adapt tests to maintain their original intent rather than removing them

Example:
```javascript
// GOOD: Using standard patterns for describe operations
Scenario: describe connections
  When I describe the connection
  Then I should get response of type "Array"

// INSTEAD OF: Creating custom step definitions
Scenario: Managing connections
  Given I create a Direct Connect connection with name prefix "aws-sdk-js"
  Then I should get a Direct Connect connection ID
  And I describe the connection
  ...

// GOOD: Testing both enabled and disabled states
it('translates empty strings when convertEmptyValues is true', -> ...)
it('does not translate empty strings when convertEmptyValues is false', -> ...)
```
