---
title: Use structured API parameters
description: When designing APIs with multiple related parameters, especially optional
  ones like filters, sorting, and pagination options, bundle them into structured
  types rather than using long parameter lists. This prevents parameter confusion,
  reduces the likelihood of argument order mistakes, and makes APIs more extensible
  without breaking changes.
repository: gravitational/teleport
label: API
language: Go
comments_count: 3
repository_stars: 19109
---

When designing APIs with multiple related parameters, especially optional ones like filters, sorting, and pagination options, bundle them into structured types rather than using long parameter lists. This prevents parameter confusion, reduces the likelihood of argument order mistakes, and makes APIs more extensible without breaking changes.

**Problems with long parameter lists:**
- Parameter confusion: `ListAccessListsWithFilter(ctx, pageSize, pageToken, search, sortBy)` - which string parameter is which?
- Difficult extension: Adding new optional parameters requires changing all call sites
- Type safety issues: Multiple parameters of the same type can be accidentally swapped

**Recommended approach:**
```go
// Instead of:
func ListBotInstances(ctx context.Context, botName string, pageSize int, lastToken string, search string, sort *types.SortBy, query string) ([]*machineidv1.BotInstance, string, error)

// Use structured parameters:
type ListBotInstancesRequest struct {
    BotName   string
    PageSize  int
    LastToken string
    Search    string
    Sort      *types.SortBy
    Query     string
}

func ListBotInstances(ctx context.Context, req *ListBotInstancesRequest) ([]*machineidv1.BotInstance, string, error)
```

For APIs with many optional parameters, consider using functional options pattern:
```go
func RangeAccessLists(ctx context.Context, start, end string, opts ...RangeOption) iter.Seq2[*accesslist.AccessList, error]
```

This approach makes APIs self-documenting, prevents argument order mistakes, and allows for backward-compatible extension of functionality.