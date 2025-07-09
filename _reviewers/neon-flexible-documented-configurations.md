---
title: Flexible documented configurations
description: 'Create configuration interfaces that are flexible, well-documented,
  and future-proof. When designing configuration parameters:


  1. **Prefer flexible parameterization** - Use functions/interfaces with optional
  parameters and sensible defaults rather than separate specialized functions for
  related configuration operations.'
repository: neondatabase/neon
label: Configurations
language: Other
comments_count: 5
repository_stars: 19015
---

Create configuration interfaces that are flexible, well-documented, and future-proof. When designing configuration parameters:

1. **Prefer flexible parameterization** - Use functions/interfaces with optional parameters and sensible defaults rather than separate specialized functions for related configuration operations.

```sql
-- Prefer this approach:
CREATE OR REPLACE FUNCTION anon.enable_transparent_masking_superuser(
  dbname TEXT,
  toggle BOOL DEFAULT = true,
)
RETURNS VOID AS
$$
BEGIN
  EXECUTE format('ALTER DATABASE %I SET anon.transparent_dynamic_masking TO %L', dbname, toggle::text);
END;
$$
```

2. **Document the rationale** - Explain not only what a parameter does, but also why it exists and the reasoning behind its format or structure.

```
/*
 * Comma-separated list of safekeeper connection strings
 * This format allows specifying multiple connection parameters for each safekeeper
 * while maintaining backward compatibility with the host:port format
 */
```

3. **Plan for future changes** - When hardcoding values or using temporary solutions, document the limitations and potential future improvements.

4. **Consider parameter precedence** - When configurations can be specified in multiple places, establish and document clear rules about which settings take precedence.

5. **Use stable sources** - For external dependencies, prefer stable, well-maintained sources (e.g., GitHub mirrors over potentially unstable direct links).