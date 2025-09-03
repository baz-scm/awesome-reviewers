---
title: Use database transactions
description: Always use database transactions when performing operations that require
  atomicity or could create race conditions. This includes scenarios where you check
  for existence before creating/updating records, or when multiple related database
  operations must succeed or fail together.
repository: SigNoz/signoz
label: Database
language: Go
comments_count: 3
repository_stars: 23369
---

Always use database transactions when performing operations that require atomicity or could create race conditions. This includes scenarios where you check for existence before creating/updating records, or when multiple related database operations must succeed or fail together.

Follow the standard transaction pattern:
1. Begin transaction with `BeginTx()`
2. Defer rollback to handle errors
3. Explicitly commit on success

Example:
```go
func (store *store) Update(ctx context.Context, funnel *traceFunnels.StorableFunnel) error {
    tx, err := store.sqlstore.BunDB().BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback()

    // Check if funnel exists
    exists, err := tx.NewSelect().
        Model((*traceFunnels.StorableFunnel)(nil)).
        Where("name = ? AND org_id = ? AND id != ?", funnel.Name, funnel.OrgID, funnel.ID).
        Exists(ctx)
    if err != nil {
        return err
    }
    if exists {
        return errors.NewAlreadyExistsf("funnel with name already exists")
    }

    // Update the funnel
    _, err = tx.NewUpdate().
        Model(funnel).
        Where("id = ?", funnel.ID).
        Exec(ctx)
    if err != nil {
        return err
    }

    return tx.Commit()
}
```

This prevents race conditions where another process could create a conflicting record between the existence check and the update operation.