---
title: Verify algorithmic equivalence
description: When replacing an exact check or well-defined numeric algorithm with
  an optimized, approximated, or restructured version (e.g., a bit-length shortcut
  instead of a direct comparison, or a rewritten normalization loop), you must prove
  or thoroughly test that the new logic is mathematically equivalent to the original
  across all boundary values, not just...
repository: python/cpython
label: Algorithms
language: Python
comments_count: 5
repository_stars: 77696
---

When replacing an exact check or well-defined numeric algorithm with an optimized, approximated, or restructured version (e.g., a bit-length shortcut instead of a direct comparison, or a rewritten normalization loop), you must prove or thoroughly test that the new logic is mathematically equivalent to the original across all boundary values, not just typical cases. Favor a provable inequality and fall back to the exact (even if slower) computation when the approximation is ambiguous, rather than shipping a "probably correct" shortcut.

For example, when checking `q < 10**prec` for a large integer `q`, a bit-length-based shortcut like `q.bit_length() < 1 + prec * _LOG_10_BASE_2` is not a safe stand-in unless you can prove it never disagrees with the exact check at the boundary. Prefer an approach like:

```python
def _is_less_than_pow10(q: int, prec: int) -> bool:
    # fast-path using a provably correct bound
    if q.bit_length() < prec * _LOG_10_BASE_2:   # _LOG_10_BASE_2 <= log2(10)
        return True
    if q.bit_length() >= 1 + prec * _LOG_10_BASE_2_UPPER:  # >= log2(10)
        return False
    # ambiguous region: fall back to the exact check
    return len(str(q)) <= prec
```

This same discipline applies to:
- Degenerate/edge-case inputs: explicitly clamp values that could otherwise produce zero, negative, or unbounded results (e.g., `splitpoint = max(1, maxchars)`) to avoid infinite loops or invalid states, rather than patching the loop after the fact.
- Refactoring numeric normalization algorithms (e.g., converting mixed float/int units into a single base unit): preserve the exact rounding and truncation semantics of the original/reference implementation (such as the C implementation), especially for mixed int/float inputs and int subclasses with custom `__mul__`/`__divmod__`.
- Type/structure traversal algorithms (e.g., MRO computation, `isinstance`/`issubclass` substitutions): confirm that a "more idiomatic" check is actually behaviorally equivalent by testing against the full range of inputs (including non-`type` generic aliases), since seemingly equivalent checks can diverge for edge-case data structures.

In all cases, add targeted tests for the boundary/edge conditions that motivated the change, and document the reasoning (ideally with a short proof or reference) so future maintainers understand why the specific bound or fallback was chosen.