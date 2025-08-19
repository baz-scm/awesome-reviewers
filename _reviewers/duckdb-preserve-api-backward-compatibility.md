---
title: Preserve API backward compatibility
description: When modifying existing APIs, ensure that current usage patterns continue
  to work unchanged. This applies to command-line interfaces, library APIs, REST endpoints,
  and any client-facing interfaces. Always provide migration paths that maintain existing
  behavior while introducing improvements.
repository: duckdb/duckdb
label: API
language: Python
comments_count: 2
repository_stars: 32061
---

When modifying existing APIs, ensure that current usage patterns continue to work unchanged. This applies to command-line interfaces, library APIs, REST endpoints, and any client-facing interfaces. Always provide migration paths that maintain existing behavior while introducing improvements.

For command-line tools, use positional arguments and optional flags that preserve the original calling convention:

```python
# Good: Maintains backward compatibility
parser.add_argument('revision', nargs='?', default='HEAD', help='Git revision to check (default: HEAD)')
parser.add_argument('directories', nargs='*', help='Directories to format')

# This allows both:
# python format.py HEAD  (original usage)
# python format.py --revision HEAD dir1 dir2  (new usage)
```

Before making API changes, identify all existing usage patterns and ensure they remain functional. Document any new capabilities as additive features rather than replacements. This principle helps maintain user trust and reduces friction during upgrades.