---
title: Database query parameter hygiene
description: Ensure all database query parameters serve a clear purpose and are properly
  utilized. Remove unused filter parameters that create confusion and verify that
  necessary filtering conditions are not accidentally omitted during refactoring.
repository: gravitational/teleport
label: Database
language: Go
comments_count: 2
repository_stars: 19109
---

Ensure all database query parameters serve a clear purpose and are properly utilized. Remove unused filter parameters that create confusion and verify that necessary filtering conditions are not accidentally omitted during refactoring.

When working with database queries and filters:
1. **Verify filter usage**: Ensure all filter parameters are actually consumed by the query logic
2. **Remove unused parameters**: Clean up vestigial parameters from previous iterations that no longer serve a purpose
3. **Validate filter conditions**: Double-check that important filtering conditions (like membership type checks) are not accidentally removed during code changes
4. **Clarify filtering responsibilities**: Be explicit about whether filtering should occur at the database/cache layer or the RPC/service layer

Example of problematic code:
```go
// Bad: unused filter parameter
func (c *Cache) RangeAccessLists(ctx context.Context, start string, end string, filter *accesslistv1.AccessListsFilter, sort *types.SortBy) {
    // filter parameter is never used in the implementation
}

// Bad: missing important filter condition
for _, owner := range existingAccessList.Spec.Owners {
    // Missing check for owner.MembershipKind == accesslist.MembershipKindList
    if err := a.updateAccessListOwnerOf(ctx, accessList.GetName(), owner.Name, false); err != nil {
        return trace.Wrap(err)
    }
}
```

This practice prevents both performance issues from unused parameters and correctness issues from missing filter conditions.