---
title: ensure migration idempotency
description: Database migrations must be designed to run safely multiple times without
  causing errors or data corruption. This involves using structured migration APIs
  instead of raw SQL, implementing proper checks for existing state, and avoiding
  unnecessary complexity that could lead to failures.
repository: SigNoz/signoz
label: Migrations
language: Go
comments_count: 4
repository_stars: 23369
---

Database migrations must be designed to run safely multiple times without causing errors or data corruption. This involves using structured migration APIs instead of raw SQL, implementing proper checks for existing state, and avoiding unnecessary complexity that could lead to failures.

Key practices:
- Use built-in migration methods like `NewDropColumn`, `NewAddColumn` instead of executing raw SQL queries for better safety and maintainability
- Implement idempotent operations that check for existing state before making changes (e.g., `IF NOT EXISTS` clauses)
- Simplify migration logic by only including necessary operations - avoid extracting unused constraints or implementing unused down migrations
- Structure migration functions to handle repeated execution gracefully

Example of idempotent migration pattern:
```go
func (migration *example) Up(ctx context.Context, db *bun.DB) error {
    // Use structured API with safety checks
    _, err := tx.NewCreateTable().
        Model((*ExampleModel)(nil)).
        IfNotExists().  // Idempotent check
        Exec(ctx)
    
    // Avoid unnecessary complexity - only pass required constraints
    column := &sqlschema.Column{
        Name:     sqlschema.ColumnName("new_field"),
        DataType: sqlschema.DataTypeText,
        Nullable: true,
    }
    // Pass nil for constraints if none needed, don't extract unused ones
    sqls := migration.sqlschema.Operator().AddColumn(table, nil, column, nil)
}

func (migration *example) Down(ctx context.Context, db *bun.DB) error {
    // Simply return nil if down migrations aren't used
    return nil
}
```

This approach ensures migrations can be run reliably across different environments and deployment scenarios without manual intervention or risk of failure.