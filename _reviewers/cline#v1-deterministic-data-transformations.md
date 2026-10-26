---
title: Deterministic Data Transformations
description: When algorithms depend on transforming external or semi-structured data
  (git status/diff outputs, metadata blobs, paths, prompts), make those transformations
  deterministic and invariant-preserving.
repository: cline/cline#v1
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 70862
---

When algorithms depend on transforming external or semi-structured data (git status/diff outputs, metadata blobs, paths, prompts), make those transformations deterministic and invariant-preserving.

Practical rules:
- **Parse with protocol-accurate splitting.** If an output format is tab/record-based, split only where the grammar says (e.g., first two `\t` fields, keep the remainder as the filename). Add tests for tricky filenames (tabs, renames/copies).
- **Preserve semantic identity across representations.** For rename/copy, don’t lose the “original path” needed for later diff/unstage steps—carry it through your parsed model.
- **Normalize paths/text deterministically.** Convert platform-specific separators to a canonical form before matching/indexing; handle edge cases like literal backslashes in POSIX filenames.
- **Validate and tolerate malformed records.** For untrusted/session metadata, drop invalid entries rather than letting them break selection logic; use explicit, stable ordering (`sort`) and selection (`reduce`/`find`) with clear semantics tied to failure/availability.
- **Use deterministic hashing/serialization for IDs/caching.** If ids are derived from content, ensure stable input normalization (sorted object keys) and enforce bounds (clip prompt fields before hashing).

Example pattern (stable parse + deterministic id):
```ts
function stableJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(stableJson).join(",")}]`;
  if (typeof value === "object" && value !== null) {
    const record = value as Record<string, unknown>;
    const fields = Object.keys(record)
      .filter((k) => record[k] !== undefined)
      .sort()
      .map((k) => `${JSON.stringify(k)}:${stableJson(record[k])}`);
    return `{${fields.join(",")}}`;
  }
  return JSON.stringify(value) ?? "null";
}

function deterministicId(kind: string, prompt: string): string {
  const clippedPrompt = prompt.trim().slice(0, 200); // enforce published bounds
  return fnv1a32(`${kind}:${clippedPrompt}`);
}
```

Apply this standard whenever your code turns strings/paths/records into structured data that other algorithmic steps rely on.