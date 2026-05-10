---
title: Self-Documenting Naming Rules
description: 'Use self-documenting identifiers: variable/function/class names should
  explain intent without relying on comments, and avoid confusing or ambiguous abbreviations.'
repository: TheAlgorithms/Python
label: Naming Conventions
language: Python
comments_count: 9
repository_stars: 220912
---

Use self-documenting identifiers: variable/function/class names should explain intent without relying on comments, and avoid confusing or ambiguous abbreviations.

Practical rules:
- Prefer descriptive `snake_case` names for functions, parameters, and local variables (e.g., `duration`, `return_period`, `step_size`).
- Avoid single-letter identifiers for semantic values (use them only for loop counters like `i`/`j` in short loops).
- Do not shadow Python built-ins or common library names (e.g., avoid naming variables/params `sort`).
- If a comment says what a variable means, rename the variable to make that comment unnecessary.

Example (before/after):
```python
# Before
def trapezoidal_rule(f, boundary, steps):
    h = (boundary[1] - boundary[0]) / steps
    a = boundary[0]
    b = boundary[1]
    x_i = make_points(a, b, h)

# After
def trapezoidal_rule(
    f: callable,
    boundary: list[float],
    steps: int,
) -> float:
    lower_bound, upper_bound = boundary
    step_size = (upper_bound - lower_bound) / steps
    x_points = make_points(lower_bound, upper_bound, step_size)
    result = 0.0
    # ...
    return result
```
Apply the same principle to all algorithm modules: ensure names are clear to someone who only reads the code.