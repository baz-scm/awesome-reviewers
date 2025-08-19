---
title: Maintain consistent naming patterns
description: Ensure all new functions, files, and identifiers follow established naming
  conventions within the codebase. This prevents naming conflicts, maintains API consistency,
  and improves code readability.
repository: duckdb/duckdb
label: Naming Conventions
language: Json
comments_count: 3
repository_stars: 32061
---

Ensure all new functions, files, and identifiers follow established naming conventions within the codebase. This prevents naming conflicts, maintains API consistency, and improves code readability.

For API functions, consistently use the established prefix pattern. For example, instead of `arrow_to_duckdb_schema`, use `duckdb_schema_from_arrow` to maintain the `duckdb_` prefix convention. Similarly, prefer descriptive names like `duckdb_value_to_string` over `duckdb_to_sql_string` to clearly indicate what the function operates on.

File names should also reflect their contents accurately - rename files like `new_vector_types.json` to `new_vector_functions.json` when the content changes to include functions rather than just types.

Deviating from established patterns can cause integration issues for clients that expect consistent naming conventions, especially when generating bindings that assume specific prefixes.