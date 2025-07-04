---
title: Database API abstraction
description: When designing database interaction layers, carefully consider when to
  create wrapper methods versus allowing direct use of underlying libraries. Add abstraction
  only when it provides significant value through error handling, feature consolidation,
  or version compatibility management.
repository: pola-rs/polars
label: Database
language: Python
comments_count: 3
repository_stars: 34296
---

When designing database interaction layers, carefully consider when to create wrapper methods versus allowing direct use of underlying libraries. Add abstraction only when it provides significant value through error handling, feature consolidation, or version compatibility management.

For instance, instead of implementing a simple wrapper method like:

```python
def write_iceberg(self, table, mode: Literal["append", "overwrite"]):
    data = self.to_arrow()
    if mode == "append":
        table.append(data)
    else:
        table.overwrite(data)
```

Consider whether users could just as easily write:
```python
# Direct usage without wrapper
table.append(df.to_arrow())
# or
table.overwrite(df.to_arrow())
```

Create wrappers when they provide meaningful value, such as handling version compatibility:

```python
if parse_version(cx.__version__) < (0, 4, 2):
    # Handle older version with specific parameters
    tbl = cx.read_sql(
        conn=connection_uri,
        query=query,
        return_type="arrow2",
        # other parameters
    )
else:
    # Handle newer version with additional features
    tbl = cx.read_sql(
        conn=connection_uri,
        query=query,
        return_type="arrow",
        pre_execution_query=pre_execution_query,
        # other parameters
    )
```

This approach keeps your database layer clean and maintainable while still providing convenience where it truly adds value. When implementing database operations, aim for the right balance between abstraction and simplicity.