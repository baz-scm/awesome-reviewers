---
title: Precise Matching Rules
description: 'When implementing parsing/classification logic, treat the input grammar
  as a contract: (1) constrain pattern matches to the intended envelope/boundaries/character
  sets (avoid prefix/superset regexes and overly broad Unicode ranges), (2) ensure
  every computed signal/metric is actually used in the final decision, and (3) add
  targeted regression tests for each...'
repository: nousresearch/hermes-agent
label: Algorithms
language: Python
comments_count: 6
repository_stars: 221948
---

When implementing parsing/classification logic, treat the input grammar as a contract: (1) constrain pattern matches to the intended envelope/boundaries/character sets (avoid prefix/superset regexes and overly broad Unicode ranges), (2) ensure every computed signal/metric is actually used in the final decision, and (3) add targeted regression tests for each boundary/grammar edge.

Apply:
- Prefer start-anchored or fullmatch grammars over “contains” checks.
- Use tight whitelists (allowed extensions/allowed code points) and explicit boundary rules (e.g., `\b`, attribute-aware tag opening).
- For placeholder-based matching, implement placeholder semantics explicitly instead of escaping placeholders.
- Don’t compute a value (e.g., divergence age) and then only append a reason after classification—plumb it into the classifier input so the verdict changes.

Example (grammar-constrained marker stripping):
```python
import re

def strip_asr_envelope(text: str) -> str:
    # Only remove the Qwen-style start-anchored envelope, not any occurrence.
    m = re.match(r"^language\s+.*?<asr_text>", text, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return text
    # Remove the first envelope marker then keep the rest.
    return text.replace(m.group(0), "", 1).strip()
```

Checklist for PRs in this area:
- What is the exact grammar? Are patterns anchored/fullmatched?
- Are regexes/char ranges minimal (not superset)?
- Are placeholders semantic (not escaped literals)?
- Do metrics used for “WARN/ERROR/PASS” flow into the classifier, not just logs/reasons?
- Are regression tests added for the discovered edge cases (case-insensitive extensions, astral text non-emoji preservation, tag-attribute boundaries, etc.)