---
title: Simplify algorithmic implementations
description: Favor clear, simple algorithmic implementations over complex custom logic.
  When faced with algorithmic choices, prefer built-in functions, direct approaches,
  and well-structured decomposition into stages.
repository: emcie-co/parlant
label: Algorithms
language: Python
comments_count: 4
repository_stars: 12205
---

Favor clear, simple algorithmic implementations over complex custom logic. When faced with algorithmic choices, prefer built-in functions, direct approaches, and well-structured decomposition into stages.

Key principles:
1. **Use built-in functions**: Replace custom implementations with standard library functions when available
2. **Choose direct approaches**: Opt for straightforward logic over complex conditional chains
3. **Decompose complex operations**: Break multi-step algorithms into clearly named stages
4. **Use lookup tables**: Replace long conditional chains with dictionary-based approaches

Example of good decomposition (from discussion 5):
```python
# Stage 1: Gather all results
all_results = chain.from_iterable(await asyncio.gather(*tasks))

# Stage 2: Remove duplicates  
unique_results = list(set(all_results))

# Stage 3: Get top results
top_results = sorted(unique_results, key=lambda r: r.distance)[:max_terms]
```

Example of lookup table approach (from discussion 7):
```python
tests = {
    "equal_to": lambda a, b: a == b,
    "not_equal_to": lambda a, b: a != b,
    "regex": lambda a, b: re.match(str(a), str(b)),
}

for test, value in conditions.items():
    if not tests[test](value, candidate.get(field)):
        return False
```

This approach improves code maintainability, reduces bugs, and makes algorithmic intent clearer to other developers.