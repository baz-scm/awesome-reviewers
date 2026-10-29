---
title: Thorough edge-case verification
description: 'Tests should fully exercise the behavior being verified, not just a
  single happy-path value that happens to pass even without the fix. Before adding
  a test, confirm it actually fails on the old code and genuinely covers the scenario
  it claims to: include boundary values (e.g. buffer-size multiples, signed-integer
  limits, timestamps around overflow points,...'
repository: python/cpython
label: Testing
language: Python
comments_count: 14
repository_stars: 77696
---

Tests should fully exercise the behavior being verified, not just a single happy-path value that happens to pass even without the fix. Before adding a test, confirm it actually fails on the old code and genuinely covers the scenario it claims to: include boundary values (e.g. buffer-size multiples, signed-integer limits, timestamps around overflow points, zero/empty inputs), multiple representative inputs/types (e.g. bytes, bytearray, and memoryview; multiple parameter lengths, not just the minimal one), and every code path that initializes shared state (e.g. all of keys()/values()/items()/len() that populate a cache, not just one).

Assertions should check the complete expected result rather than a partial slice of it, so regressions in untested parts aren't silently missed. For example, prefer comparing a whole dict/tuple to expected values instead of checking a few keys individually:

```python
# Weak: only checks a few keys
self.assertEqual(d['a'], 3)
self.assertEqual(d['b'], 4)

# Better: verifies the entire result
self.assertEqual(d, {'a': 3, 'b': 4, 'c': 7, 'self': self})
```

Likewise, when a test simplifies away the original setup (e.g. dropping the written data from a round-trip test, or using a round timestamp that doesn't exercise the fix), make sure the simplification still proves the behavior under test — if in doubt, write the test first against the broken code and confirm it fails before confirming it passes with the fix.