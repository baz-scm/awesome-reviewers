---
title: Deterministic Parse Normalization
description: 'When writing algorithms that transform external/variable inputs (command
  output, user text/frontmatter, paths, serialized content), ensure three properties:'
repository: cline/cline#v30
label: Algorithms
language: TypeScript
comments_count: 8
repository_stars: 70894
---

When writing algorithms that transform external/variable inputs (command output, user text/frontmatter, paths, serialized content), ensure three properties:

1) Normalize and bound inputs before using them as keys or to derive stable outputs.
2) Parse using the correct record boundaries for the format (NUL-delimited, first-N tabs, structured “continuation lines”), and preserve any context required for downstream steps (e.g., rename original paths).
3) Add edge-case tests for the tricky variability that breaks naive implementations (tabs/backslashes in filenames, block vs inline scalars, missing plural categories, large payload representations).

Practical checklist:
- Hash/ID derivations: clip or sanitize fields to the published limits *before* hashing.
- Parsing CLI output: split on the format’s real delimiters (e.g., `\0` for porcelain/v1) and carefully constrain tab-splitting (e.g., split only the first two tabs, keep the rest as the filename).
- YAML/frontmatter: implement precedence explicitly and use parsing logic that matches YAML structure (inline vs block scalars; boolean spellings).
- Path handling: normalize separators without corrupting filenames that contain separator-like characters.
- Estimation/complexity: ensure the algorithm’s cost model is representation-invariant (e.g., base64 payload size shouldn’t dominate an image token estimate).

Example (stable ID with bounded inputs):
```ts
function fnv1a32(text: string): string {
  let hash = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    hash = Math.imul(hash ^ text.charCodeAt(i), 0x01000193) >>> 0;
  }
  return hash.toString(16).padStart(8, '0');
}

const PROMPT_MAX_CHARS = 2000;
const WHY_MAX_CHARS = 2000;

export function suggestionId(kind: string, prompt: string, why: string) {
  const clippedPrompt = prompt.slice(0, PROMPT_MAX_CHARS);
  const clippedWhy = why.slice(0, WHY_MAX_CHARS);
  return fnv1a32(`${kind}:${clippedPrompt}:${clippedWhy}`);
}
```

Apply this standard to any new data-processing code: first decide what must remain stable/deterministic downstream, then encode the normalization/parsing rules explicitly, and finally lock them in with edge-case tests.