---
title: Structural Normalization Rules
description: When writing algorithms that normalize or reason over structured inputs
  (schemas, message blocks, file paths, or change previews), base decisions on the
  structure/invariants—not on superficial representations—and ensure recursion/processing
  reaches nested forms.
repository: cline/cline#v3
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 70863
---

When writing algorithms that normalize or reason over structured inputs (schemas, message blocks, file paths, or change previews), base decisions on the structure/invariants—not on superficial representations—and ensure recursion/processing reaches nested forms.

Apply these rules:
- **Recurse through nested containers before gating.** If your logic has conditions like “is this object-like?”, don’t apply them before normalizing nested `items`/branches—otherwise deep cases will be missed.
- **Use structural estimators with complexity bounds.** Token/cost estimation should scale with the counted structural units (e.g., number of images), not with incidental payload representation (e.g., base64 string length).
- **Normalize paths deterministically and literally.** Convert to the target format (e.g., POSIX) without breaking filenames containing separator-like literals (e.g., a literal backslash).
- **Validate tool semantics with targeted tests.** If you’re relying on specific behavior of an external algorithm/tool (e.g., Git plumbing), cover it with tests that match real scenarios.

Example (recursive schema normalization pattern):
```ts
function normalizeType(schema: any): any {
  const s = { ...schema };

  // Always recurse into known nested forms first
  if (s.items) s.items = normalizeType(s.items);
  for (const k of ["anyOf", "oneOf", "allOf"]) {
    if (Array.isArray(s[k])) s[k] = s[k].map(normalizeType);
  }

  // Then apply object-like gating / local normalization
  if (typeof s.type === "string") s.type = s.type.toLowerCase();
  const isObjectLike =
    s.type === "object" ||
    "properties" in s ||
    "required" in s ||
    "additionalProperties" in s;

  if (!isObjectLike) return s;
  if (s.properties) {
    for (const [key, value] of Object.entries(s.properties)) {
      s.properties[key] = typeof value === "object" && value
        ? normalizeType(value)
        : value;
    }
  }
  return s;
}
```

Checklist for PRs in this area:
- Are nested structures fully traversed (arrays/items + combinators/branches)?
- Are estimates bounded and based on structural units rather than payload sizes?
- Is path/text normalization literal-safe across platforms?
- Do tests include edge cases that would fail naive assumptions (deep nesting, tricky literals, realistic tool scenarios)?