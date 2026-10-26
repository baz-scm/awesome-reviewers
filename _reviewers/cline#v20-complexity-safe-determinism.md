---
title: Complexity-Safe Determinism
description: When implementing non-trivial algorithms (IDs, token estimates, parsing/filtering),
  ensure results are deterministic and robust under worst-case inputs.
repository: cline/cline#v20
label: Algorithms
language: TypeScript
comments_count: 7
repository_stars: 70886
---

When implementing non-trivial algorithms (IDs, token estimates, parsing/filtering), ensure results are deterministic and robust under worst-case inputs.

**Standards**
1) **Cap/normalize before deriving outputs** (IDs, hashes, cost estimates, search keys). Derive from a bounded representation so published limits and fixture parity hold.
2) **Prevent payload-sized scaling**: base64/image/text blobs should not drive linear cost estimates if the real billing/model cost is capped per item/type.
3) **Use stateful parsing/pairing for log or multi-record formats** rather than one-shot regex “filters”. Pair start/end events by identity and order; handle multi-record rename/copy sequences by consuming subsequent records.
4) **Be complexity-safe**: avoid regex patterns that can backtrack poorly; prefer linear scans/loops and enforce explicit limits (bytes, link depth, buffer sizes).
5) **Test invariants and edge cases**: add regression tests for known pathological shapes and (where feasible) property/fuzz tests for ordering/pagination/drop/undo rules.

**Example pattern (bounded deterministic hash)**
```ts
const PROMPT_MAX_CHARS = 200;
const WHY_MAX_CHARS = 400;

function hash32(text: string): string {
  // FNV-1a style placeholder
  let h = 0;
  for (let i = 0; i < text.length; i++) h = (h * 33 + text.charCodeAt(i)) >>> 0;
  return h.toString(16).padStart(8, "0");
}

export function suggestionId(kind: string, prompt: string, why: string) {
  const p = prompt.slice(0, PROMPT_MAX_CHARS);
  const w = why.slice(0, WHY_MAX_CHARS);
  return hash32(`${kind}:${p}:${w}`);
}
```

Apply this style to token estimation, log/report filtering, and multi-record parsers so correctness doesn’t degrade (or become expensive) with adversarial or simply large inputs.