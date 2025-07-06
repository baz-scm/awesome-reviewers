---
title: Use specific assertions
description: Always write assertions that verify specific, expected values rather
  than simple existence or boolean checks. This ensures tests validate exactly what
  you intend and provides clearer error messages when tests fail.
repository: octokit/octokit.net
label: Testing
language: C#
comments_count: 8
repository_stars: 2793
---

Always write assertions that verify specific, expected values rather than simple existence or boolean checks. This ensures tests validate exactly what you intend and provides clearer error messages when tests fail.

**Do this:**
```csharp
// Use Assert.Equal to get both values when the test fails
Assert.Equal(2, issue.Assignees.Count);
Assert.Equal(_context.RepositoryOwner, closed.Assignees[0].Login);
```

**Not this:**
```csharp
// Provides less helpful error messages
Assert.True(issue.Assignees.Count == 2);
Assert.True(closed.Assignees[0].Login == _context.RepositoryOwner);
```

When testing state changes, verify the specific new values rather than just checking the count:
```csharp
// Verify the specific team that should be present after a change
Assert.Contains(restrictions, team => team.Name == contextOrgTeam2.TeamName);
// Rather than just checking the count which could be correct by coincidence
Assert.Equal(1, restrictions.Count);
```

In method tests, assert on exact return values, not just that a method was called. For object state assertions, verify the fields that should have changed rather than just checking if an object is non-null.

By being specific in your assertions, you:
1. Create tests that clearly document expectations
2. Get more helpful error messages showing both expected and actual values
3. Avoid false positives where tests pass despite functional failures
4. Make it easier to diagnose failures when tests eventually break