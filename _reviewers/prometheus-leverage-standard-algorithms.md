---
title: leverage standard algorithms
description: When implementing common algorithmic tasks like string parsing, sorting,
  or comparison operations, prefer built-in utilities and standard library functions
  over custom implementations. Standard algorithms are typically more efficient, well-tested,
  and maintainable than custom solutions.
repository: prometheus/prometheus
label: Algorithms
language: Shell
comments_count: 2
repository_stars: 59616
---

When implementing common algorithmic tasks like string parsing, sorting, or comparison operations, prefer built-in utilities and standard library functions over custom implementations. Standard algorithms are typically more efficient, well-tested, and maintainable than custom solutions.

For string parsing, use built-in shell features:
```bash
# Instead of multiple parameter expansions:
major=${current_full_version%%.*}
minor=${current_full_version#*.}; minor=${minor%%.*}

# Use single-line built-in parsing:
IFS='.' read -r major minor _ <<< "$(go mod edit -json go.mod | jq -r .Go)"
```

For version comparison, leverage system utilities:
```bash
# Instead of custom compare_versions() function:
if ! echo -e "${min_version}\n${version}" | sort --version-sort --check=silent; then
    # handle version mismatch
fi
```

This approach reduces code complexity, improves reliability, and often provides better performance than reinventing common algorithmic patterns.