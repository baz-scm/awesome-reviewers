---
title: Behavioral Regression Testing
description: 'When adding or modifying tests, favor *behavioral contract* coverage
  over brittle implementation/shape checks.


  Apply these rules:

  - **Test the outcome, not the shape**: drive the code through the real wiring/dispatch
  path and assert the externally observable behavior (e.g., callback fires once after
  a cap; command output path rewrites; retry-after falls...'
repository: nousresearch/hermes-agent
label: Testing
language: Python
comments_count: 9
repository_stars: 221948
---

When adding or modifying tests, favor *behavioral contract* coverage over brittle implementation/shape checks.

Apply these rules:
- **Test the outcome, not the shape**: drive the code through the real wiring/dispatch path and assert the externally observable behavior (e.g., callback fires once after a cap; command output path rewrites; retry-after falls back correctly). Avoid “predicate-only” tests when the bug is in integration/wiring.
- **Avoid change-detector tests**: do not pin production behavior by parsing/regex-reading source files, matching exact allowlist snapshots, or asserting on internal code markers that can change without breaking behavior.
- **Make timing deterministic**: never rely on platform sleep/clock resolution for pass/fail. Use a fake monotonic clock (or backdate timestamps deterministically) so assertions don’t vary by OS/filesystem.

Example pattern (deterministic time):
```python
class FakeTime:
    def __init__(self, real_time, start=1000.0):
        self._real = real_time
        self._now = start
    def monotonic(self):
        return self._now
    def advance(self, seconds):
        self._now += seconds
    def __getattr__(self, name):
        return getattr(self._real, name)

def test_silence_threshold(monkeypatch):
    import time as real_time
    fake = FakeTime(real_time)
    monkeypatch.setattr("tools.voice_mode.time", fake)
    # drive the timeline deterministically
    fake.advance(0.05)
    # assert state transitions...
```

This approach makes tests resilient to harmless refactors while still catching real regressions in control flow, branching, and platform-dependent behavior.