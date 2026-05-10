---
title: Validate Inputs Explicitly
description: Enforce each function’s documented input contract with early, explicit
  checks; raise specific exceptions with accurate messages (avoid asserts, silent
  fallbacks/defaults, and misleading error paths after normalization). Keep try/except
  blocks as narrow as possible—only around the operations that can fail.
repository: TheAlgorithms/Python
label: Error Handling
language: Python
comments_count: 11
repository_stars: 220912
---

Enforce each function’s documented input contract with early, explicit checks; raise specific exceptions with accurate messages (avoid asserts, silent fallbacks/defaults, and misleading error paths after normalization). Keep try/except blocks as narrow as possible—only around the operations that can fail.

Guideline checklist:
- Align runtime validation with docstrings and examples (if doc says “non-negative s”, reject s_value < 0).
- Validate relationships/ranges using a single correct predicate (e.g., reject values where a computed sine is not within [-1, 1]).
- Prefer ValueError/TypeError over assert; never rely on assertions for user-facing correctness.
- Do not silently change behavior for invalid configuration (raise ValueError instead of defaulting mode).
- After normalization (strip sign/whitespace), ensure the error message still matches the actual failing condition.
- For CLI/I/O parsing, limit try/except to the conversion line(s); don’t wrap the whole program.

Example pattern:
```py
import math

def calculate_refraction_angle(n1: float, n2: float, incident_angle_degrees: float) -> float:
    # precondition: physical/numerical domain
    if n1 <= 0 or n2 <= 0:
        raise ValueError("Refractive indices must be positive")

    theta1 = math.radians(incident_angle_degrees)
    refraction_sine = (n1 / n2) * math.sin(theta1)

    # physical validity in one place; message stays truthful
    if not -1.0 <= refraction_sine <= 1.0:
        raise ValueError("Total Internal Reflection or invalid physical inputs")

    return math.degrees(math.asin(refraction_sine))
```

Apply the same approach across data structures and educational utilities: validate configuration (raise on invalid mode), validate parameter types/relationships, and make failure modes deterministic and easy to understand.