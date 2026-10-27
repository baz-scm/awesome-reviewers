---
title: Null Safety Invariants
description: When handling potentially-null/undefined values, don’t just add generic
  null checks—first ensure you’re reading from the correct owning object/shape, then
  explicitly handle the allowed null states, and fail loudly for states that should
  be impossible.
repository: facebook/react#b14
label: Null Handling
language: JavaScript
comments_count: 8
repository_stars: 251893
---

When handling potentially-null/undefined values, don’t just add generic null checks—first ensure you’re reading from the correct owning object/shape, then explicitly handle the allowed null states, and fail loudly for states that should be impossible.

**Standards**
1. **Use the correct discriminator/owner before dereference**
   - If a property can be null depending on runtime shape, branch on that discriminator (e.g., `nodeType`) or use the helper that already encodes the owning-root logic.
2. **Initialize nullable variables to match their declared union**
   - Don’t rely on implicit `undefined` when the union says `null | T` (or vice versa). Initialize explicitly.
3. **Fail loudly for “should never happen” structures**
   - If types/state imply a value’s internal shape, don’t silently continue with optional chaining; prefer invariant/throw so hook/tree parsing bugs surface.
   - If behavior is intentionally a noop for user-facing API semantics (e.g., unmounted host methods), keep it consistent with existing behavior, but document/justify it.
4. **Prefer null checks that match types and intent**
   - Use `=== null` / `=== undefined` (or a single idiom) when the type tells you what’s possible; avoid mixed/ambiguous comparisons.

**Example pattern (nodeType-based null safety)**
```js
function getOwnerDocument(otherNode: any) {
  return otherNode.nodeType === DOCUMENT_NODE
    ? (otherNode: any) // ownerDocument is null on the document itself
    : otherNode.ownerDocument;
}

const ownerDocument = getOwnerDocument(otherNode);
const activeElement = ownerDocument && ownerDocument.activeElement;
if (activeElement == null) {
  return; // explicitly handle the nullish case
}
```

Apply these rules during code review: (a) identify which runtime shapes make a value nullable, (b) branch based on that shape/discriminator (or correct helper), (c) align initializations and null checks with the declared types, and (d) crash for invariant violations instead of silently masking them.