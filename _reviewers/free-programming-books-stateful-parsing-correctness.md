---
title: Stateful Parsing Correctness
description: When implementing stateful parsing (e.g., direction/context tracking
  with stacks), treat correctness as a property of the whole scan loop—not just the
  “main” match.
repository: EbookFoundation/free-programming-books
label: Algorithms
language: Python
comments_count: 2
repository_stars: 388003
---

When implementing stateful parsing (e.g., direction/context tracking with stacks), treat correctness as a property of the whole scan loop—not just the “main” match.

Apply these rules:
- Don’t use `continue` (or similar early-skip control flow) in ways that prevent subsequent tokens/characters on the same iteration/input segment from being processed. If multiple tags/tokens can exist close together, ensure nothing that could affect output/state is skipped.
- If a line can contain multiple relevant tags, extract *all* matches on that line and process them in textual order, updating your context stack deterministically (push on opening, pop on closing).
- Document the intent (especially why multiple tags on the same line must be handled) and the meaning of match groups/tuples so future edits don’t regress correctness.

Example pattern (process all `<div dir>` tags on a line, in order):
```py
# Find all opening and closing <div> tags on the line
div_tags = re.findall(
    r"(<div[^>]*dir=['\"](rtl|ltr)['\"][^>]*>|</div>)",
    line,
    re.IGNORECASE,
)

for tag, direction in div_tags:
    if tag.startswith('<div') and 'markdown="1"' in tag:
        block_context_stack.append(direction.lower())
    elif tag == '</div>' and len(block_context_stack) > 1:
        block_context_stack.pop()
```

Add/keep tests that cover: (1) multiple tags on the same line and (2) cases where skipping tokens would drop nearby output characters (e.g., punctuation around inline spans).