---
title: Deterministic Mapping Pipeline
description: 'When implementing parsing/storage/retrieval logic (or any pipeline with
  downstream queries), design the algorithm so that *representations, keys, and batching
  decisions are stable and consistent*:'
repository: infiniflow/ragflow
label: Algorithms
language: Python
comments_count: 5
repository_stars: 80174
---

When implementing parsing/storage/retrieval logic (or any pipeline with downstream queries), design the algorithm so that *representations, keys, and batching decisions are stable and consistent*:

- **Preserve representation contracts:** If downstream search/filter expects tokenized fields (e.g., `*_tks`), never “simplify” stored values to raw strings for those fields.
  - For mixed needs (human-readable + search tokens), **store parallel values** (e.g., tokenized for vector/search fields, raw for metadata display/aggregation).
- **Use authoritative mappings; avoid brittle inference:** If the KB/task snapshot already contains the correct `field_map`/column-to-typed-key mapping, load it rather than guessing via suffix/fuzzy matching (especially for non-ASCII/Pinyin-derived keys). Keep inference/probing only as a last-resort fallback when the authoritative data is unavailable.
- **Implement bounded windowing explicitly:** For batched/chunked processing, compute and pass explicit window bounds (e.g., `page_to = min(page_from + batch, total_pages)`) to avoid default truncation.
- **Make quality gates deterministic:** Any detector used to decide OCR vs text (e.g., garbled-page detection) must be deterministic—remove randomness from sampling or make it repeatable (e.g., `s[:N]` instead of `random.sample`). Prefer thresholding to reduce false positives.

Example pattern (parallel token/raw + bounded, deterministic detection):

```python
# 1) Parallel values: keep token fields tokenized
if role in ("vectorize", "both"):
    chunk[f"{typed_key}_tks"] = tokenize(value)
if role in ("metadata", "both"):
    chunk[f"_raw_{col}"] = str(value)  # human-readable for aggregation/UI

# 2) Bounded windowing
for page_from in range(0, total_pages, batch_size):
    page_to = min(page_from + batch_size, total_pages)
    load_pages(page_from=page_from, page_to=page_to)

# 3) Deterministic detector sampling
sample = page_chars[:200]  # not random.sample
is_garbled = detect(sample, threshold=0.3)
```

Adopting this standard prevents subtle retrieval/search regressions, reduces heuristic flakiness, and improves correctness/performance of chunked algorithms.