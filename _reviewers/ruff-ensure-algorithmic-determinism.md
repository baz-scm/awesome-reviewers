---
title: Ensure algorithmic determinism
description: When implementing algorithms for code analysis, type checking, or pattern
  matching, ensure they produce consistent and deterministic results for the same
  inputs. Edge cases should be explicitly handled rather than making assumptions.
repository: astral-sh/ruff
label: Algorithms
language: Other
comments_count: 3
repository_stars: 40619
---

When implementing algorithms for code analysis, type checking, or pattern matching, ensure they produce consistent and deterministic results for the same inputs. Edge cases should be explicitly handled rather than making assumptions.

Key practices:
1. Use deterministic data structures when order matters (e.g., IndexMap instead of HashMap when processing needs to be order-sensitive)
2. Validate success conditions explicitly rather than assuming failure
3. Test edge cases thoroughly to prevent unexpected behavior

Example of problematic code:
```python
# Incorrect: Unconditionally reporting error without checking if a match was found
def check_overloads(call_site, overloads):
    for overload in overloads:
        if arity_matches(call_site, overload):
            # Missing validation! We found a potential match but didn't verify it
            pass
    # Incorrectly assumes failure even when a match might exist
    report_no_matching_overload(call_site)
```

Improved implementation:
```python
# Correct: Explicitly track success and only report error when needed
def check_overloads(call_site, overloads):
    potential_matches = []
    for overload in overloads:
        if arity_matches(call_site, overload):
            potential_matches.append(overload)
    
    # Only report error if truly no matches were found
    if not potential_matches:
        report_no_matching_overload(call_site)
    else:
        # Process potential matches further
        validate_matches(call_site, potential_matches)
```

Non-deterministic algorithms can introduce subtle bugs that are difficult to reproduce and debug. By ensuring deterministic behavior and explicit validation of conditions, you can create more robust and maintainable code.