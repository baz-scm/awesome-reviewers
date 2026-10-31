---
title: Harden security pattern matching
description: When writing security-critical matching logic—command blocklists/allowlists,
  path sandboxing, or any pattern-based access control—treat both false negatives
  (bypasses) and false positives (over-blocking) as bugs, and prove it with tests,
  not inspection alone.
repository: kyegomez/swarms#pi240310
label: Security
language: Python
comments_count: 16
repository_stars: 7337
---

When writing security-critical matching logic—command blocklists/allowlists, path sandboxing, or any pattern-based access control—treat both false negatives (bypasses) and false positives (over-blocking) as bugs, and prove it with tests, not inspection alone.

- For every new or changed pattern, add parametrized tests for the specific bypass it could introduce (wrapper commands like `nice`/`timeout`/`sh -c`, quoting/escaping, word-boundary edge cases such as `su` vs `su-exec` or `mkfs` vs `mkfs.ext4`, case folding) and for the legitimate inputs it must not block. Don't rely on "it looks anchored" reasoning—run the regex against the adversarial examples raised in review.
- Keep normalization consistent across all branches of the same check: if one part of the validator lowercases or folds the input, every other part checking the same data should do the same (or document why not), so the whole function reasons about one canonical string.
- Guard against catastrophic backtracking when combining quantifiers over alternations (e.g. `(?:\w+=\S*\s+|-\S*\s+|\d\S*\s+)*`). Make alternatives mutually exclusive or bound repetition, and benchmark the check against a long adversarial string (e.g. thousands of repeated separator/assignment tokens) before merging.
- When a value is validated (e.g. a resolved filesystem path, a parsed argument), make sure the exact value that passed validation is what gets used downstream. Avoid TOCTOU gaps where you validate a `realpath` but act on the original unresolved path, and normalize for platform quirks (e.g. case-insensitive filesystems) that could cause legitimate requests to be wrongly rejected or, worse, a malicious one to slip through.
- Don't silently bundle unrelated security-policy changes (e.g. widening a length cap, loosening a bound) into a correctness fix—call it out explicitly, justify it against real consumers, and let it be reviewed on its own merits.

Example of a safer anchored word check with disjoint prefix-skipping to avoid both false positives and ReDoS:
```python
_WORD_REGEX = re.compile(
    r"(?:^|[\n;&|({!`]|\b(?:nice|timeout|sh|bash|zsh)\s)"
    r"\s*(?:\w+=\S*\s+)*"          # only assignments skipped, not open-ended flags
    r"(?:\S*/)?(?:sudo|mkfs)(?![\w.-])",
    re.IGNORECASE,
)
```
</description>
</invoke>
