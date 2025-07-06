---
title: Safe constraint modification sequence
description: 'When modifying constraints in database migrations, follow a safe sequence
  of operations to prevent integrity errors:


  1. For adding not-nullable constraints to existing tables:'
repository: apache/airflow
label: Migrations
language: Python
comments_count: 4
repository_stars: 40858
---

When modifying constraints in database migrations, follow a safe sequence of operations to prevent integrity errors:

1. For adding not-nullable constraints to existing tables:
   - First add the column as nullable
   - Populate data with appropriate values
   - Then alter the column to make it not-nullable

2. For foreign key constraints:
   - Ensure referenced and referencing columns have matching nullability
   - Drop foreign keys before changing nullability constraints
   - Recreate foreign keys after both sides match

3. For cross-database compatibility, use dialect-specific SQL when necessary:

```python
def upgrade():
    dialect_name = op.get_bind().dialect.name
    
    # Add default values to referenced table
    if dialect_name == "postgresql":
        op.execute("INSERT INTO dag_bundle (name) VALUES ('dags-folder') ON CONFLICT (name) DO NOTHING;")
    elif dialect_name == "mysql":
        op.execute("INSERT IGNORE INTO dag_bundle (name) VALUES ('dags-folder');")
    elif dialect_name == "sqlite":
        op.execute("INSERT OR IGNORE INTO dag_bundle (name) VALUES ('dags-folder');")
    
    # Modify constraints safely
    with op.batch_alter_table("dag", schema=None) as batch_op:
        # 1. Populate data first
        conn = op.get_bind()
        conn.execute(text("UPDATE dag SET bundle_name = 'dags-folder' WHERE bundle_name IS NULL"))
        
        # 2. Drop FK constraint before changing nullability
        batch_op.drop_constraint("dag_bundle_name_fkey", type_="foreignkey")
        
        # 3. Alter column nullability
        batch_op.alter_column("bundle_name", nullable=False, existing_type=sa.String(length=250))
    
    # 4. Recreate foreign key after both sides are compatible
    with op.batch_alter_table("dag", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "dag_bundle_name_fkey", "dag_bundle", ["bundle_name"], ["name"]
        )
```

For downgrades, restore schema constraints but avoid destructive data operations when possible.