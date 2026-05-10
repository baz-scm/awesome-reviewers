---
title: Pure Functions and Main Guard
description: 'Keep reusable code clean and production-ready: reusable/algorithmic
  functions should be side-effect free (no `print()`), and all executable/demo/driver
  code must be under an `if __name__ == "__main__":` guard. Also keep imports at the
  top and sorted/PEP8-compliant.'
repository: TheAlgorithms/Python
label: Code Style
language: Python
comments_count: 8
repository_stars: 220912
---

Keep reusable code clean and production-ready: reusable/algorithmic functions should be side-effect free (no `print()`), and all executable/demo/driver code must be under an `if __name__ == "__main__":` guard. Also keep imports at the top and sorted/PEP8-compliant.

Example (move prints + examples):

```python
def quick_select(items: list[int], index: int) -> int:
    # reusable logic: no printing, no prompting
    ...


def _demo() -> None:
    prices = [7, 1, 5, 3, 6, 4]
    print("Example:", quick_select(prices, 3))


if __name__ == "__main__":
    _demo()
```

Checklist:
- No `print()`/debug logging in core algorithm/library functions (return values instead).
- Put example usage, manual tests, and script entry points behind `if __name__ == "__main__":`.
- Put all imports at the top of the file; sort/group them per lint rules.
- Ensure type hints and function signatures are consistent and non-redundant (don’t omit required annotations for public functions).