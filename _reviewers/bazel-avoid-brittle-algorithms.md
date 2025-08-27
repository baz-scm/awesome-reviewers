---
title: avoid brittle algorithms
description: Replace fragile algorithmic approaches with robust, well-tested alternatives.
  Brittle algorithms that rely on manual parsing, string manipulation, or assumptions
  about data format are prone to failure and difficult to maintain.
repository: bazelbuild/bazel
label: Algorithms
language: Python
comments_count: 2
repository_stars: 24489
---

Replace fragile algorithmic approaches with robust, well-tested alternatives. Brittle algorithms that rely on manual parsing, string manipulation, or assumptions about data format are prone to failure and difficult to maintain.

When processing structured data, prefer established parsing techniques over ad-hoc string operations. For example, replace manual token splitting with regex patterns or proper parsers that handle edge cases gracefully.

Example of improvement:
```python
# Brittle approach - manual string splitting
tokens = line.split(maxsplit=2)
label = tokens[0]
if tokens[1][0] != "(" or tokens[1][-1] != ")":
    raise ValueError(f"{tokens[1]} in {line} not surrounded by parentheses")
config_hash = tokens[1][1:-1]

# Robust approach - regex matching
result = CQUERY_RESULT_LINE_REGEX.search(line)
```

Similarly, in complex systems with error propagation, design algorithms that properly store and handle errors at each layer rather than relying on fragile assumptions about error bubbling behavior. This ensures your algorithms remain reliable as the system evolves.