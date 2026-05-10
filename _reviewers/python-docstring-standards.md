---
title: Docstring Standards
description: 'Apply a single documentation rule set across the codebase:


  - **Module/file docstring:** Each file should have a clear module-level docstring
  **before any imports**.'
repository: TheAlgorithms/Python
label: Documentation
language: Python
comments_count: 19
repository_stars: 220912
---

Apply a single documentation rule set across the codebase:

- **Module/file docstring:** Each file should have a clear module-level docstring **before any imports**.
- **Docstring completeness:** Docstrings must explain *behavior*, key **assumptions** (inputs/constraints), important **units**, and any **approximation** or dependency requirements needed to use the code.
- **No type duplication:** Do **not** repeat parameter/return data types in the docstring when they are already present in the function signature (let the type hints be the source of truth).
- **Consistent style/wording:** Follow the repo’s chosen docstring convention (e.g., Sphinx-style) and ensure wording starts appropriately (for lint rules like “docstring starts with this”).
- **Doctests stay with docs:** If docstrings contain doctests that act as unit tests, keep them; add doctests to validate behavior for new functions.
- **Keep comments accurate/redundant-free:** Don’t add comments that contradict docstring intent; avoid duplicating what a docstring already explains.

Example (illustrates the “no type duplication” + clear behavior):
```py
def time_period_of_satellite(mass: float, radius: float, height: float) -> float:
    """Calculate the orbital period of a satellite.

    Uses T = 2π * sqrt((R + h)^3 / (G * M)).

    Units: mass in kg, radius/height in meters.
    """
    ...
```

Operationally: during review, enforce these as checklist items for every new/changed file and function/method docstring.