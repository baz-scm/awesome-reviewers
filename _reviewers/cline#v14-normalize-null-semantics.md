---
title: Normalize null semantics
description: Null/undefined/missing values must have a single, well-defined meaning
  end-to-end (types → validation/schema → runtime normalization → external calls).
  Avoid “accidental” semantics from defaults, `??`, schema nullability, or library
  parameter binding.
repository: cline/cline#v14
label: Null Handling
language: TypeScript
comments_count: 6
repository_stars: 70876
---

Null/undefined/missing values must have a single, well-defined meaning end-to-end (types → validation/schema → runtime normalization → external calls). Avoid “accidental” semantics from defaults, `??`, schema nullability, or library parameter binding.

Apply:
- **State the contract**: For each field, decide whether `null`, `undefined`, and “omitted” are distinct or should be treated the same (usually: treat `null` as “omitted” for create/insert operations).
- **Normalize early and match types to runtime**: If runtime normalizes `null` → omission, the TS signature must reflect `null` (not just `undefined`).
- **Don’t use `??` to detect absence** when empty is a valid value (e.g., `[]` vs missing attachments). Use length checks or explicit “was field provided” signals.
- **Be explicit with external interfaces**: Some systems treat unprefixed named parameters as `NULL` (SQL), or decode omitted protobuf fields as empty arrays—ensure your call-site matches the required contract.
- **Encode conditional presence in types**: When a field is “only set in beforeRun”, prefer a discriminated union so consumers can’t guess and accidentally treat missing as falsey.

Example (attachment retry):
```ts
async function retryWithAttachments(retry: { images: string[] }, images?: string[]) {
  // Omitted images decode as [] — length-aware merge avoids losing retry attachments.
  const finalImages = images?.length ? images : retry.images;
  return finalImages;
}
```

Example (null normalization contract):
```ts
type Input = { oldText?: string | null };
function normalizeOldText(input: Input): { oldText?: string } {
  const v = input.oldText;
  return v == null ? {} : { oldText: v }; // null/undefined => omitted
}
```