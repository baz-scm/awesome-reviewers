---
title: Deterministic Algorithm Correctness
description: 'When implementing non-trivial algorithms (graph ordering, batching under
  constraints, multi-pass transformations), apply four requirements:


  1) **Guarantee termination with explicit guards/invariants**'
repository: langchain-ai/langchain
label: Algorithms
language: Python
comments_count: 7
repository_stars: 136312
---

When implementing non-trivial algorithms (graph ordering, batching under constraints, multi-pass transformations), apply four requirements:

1) **Guarantee termination with explicit guards/invariants**
- Add edge-case checks that prevent infinite loops.
- Ensure each loop iteration makes measurable progress toward completion.

2) **Respect real constraints with dynamic computation**
- If an API has a real limit (e.g., `MAX_TOKENS_PER_REQUEST`), batch using dynamic per-item measurements (e.g., token counts), not fixed-size assumptions.

3) **Keep behavior deterministic across passes**
- If you compute node/segment identifiers in one phase and reuse them in another (e.g., graph construction vs edge building), the identifier mapping must be stable/deterministic so references match.
- Avoid patterns like per-call nondeterministic hashing for identity mapping; prefer deterministic encodings.

4) **Separate algorithm concerns into a dedicated, testable unit**
- If a function mixes dependency discovery, instantiation, graph construction, sorting, and cycle detection, extract a `Resolver/Planner` with small methods and a clean public interface (e.g., `resolve(middleware)`).

Example (token-aware batching with progress and guaranteed exit):
```python
# Precondition: token_counts and tokens are aligned
batched = []
i = 0
while i < len(tokens):
    batch_end = i + 1  # progress guarantee
    batch_token_count = token_counts[i]
    for j in range(i + 1, min(i + _chunk_size, len(tokens))):
        if batch_token_count + token_counts[j] > MAX_TOKENS_PER_REQUEST:
            break
        batch_token_count += token_counts[j]
        batch_end = j + 1

    # API call uses tokens[i:batch_end]
    response = client.create(input=tokens[i:batch_end], **client_kwargs)
    batched.append(response)
    i = batch_end
```

Example (deterministic Mermaid node label encoding):
```python
def to_safe_ascii_id(label: str) -> str:
    out = []
    for ch in label:
        if ch.isascii() and (ch.isalnum()):
            out.append(ch.lower())
        else:
            out.append('n' + format(ord(ch), 'x'))
    slug = ''.join(out)
    return slug if slug[0].isalpha() else 'n' + slug
```

Adopting these rules reduces correctness regressions (limits/termination), avoids subtle identity mismatches in graph-like structures, and makes algorithmic code easier to reason about and test.