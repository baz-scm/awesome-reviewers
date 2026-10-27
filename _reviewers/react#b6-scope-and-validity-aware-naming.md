---
title: Scope- and Validity-aware Naming
description: When generating or classifying identifiers during transformations, tie
  naming decisions to (a) what inputs are actually valid at that point in the pipeline
  and (b) the exact scope/namespace where collisions can occur.
repository: facebook/react#b6
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 251888
---

When generating or classifying identifiers during transformations, tie naming decisions to (a) what inputs are actually valid at that point in the pipeline and (b) the exact scope/namespace where collisions can occur.

Apply:
- Validate identifier eligibility before treating something as a component/reference name. If non-valid forms can’t reach the codepath (because the parser rejects them), document that precisely (“only valid identifiers reach this branch”).
- Choose a deduplication boundary that matches the transformed namespace. For example, when sanitizing JSX prop names (e.g., converting `aria-label` to a camelCased binding), dedupe based on the post-sanitization identifiers within the outlined function’s fresh scope—avoid renaming strategies that over-fire and change snapshot/eval behavior.
- Preserve semantics for names that must remain external. For hyphenated JSX props, keep the original attribute name at the call site and use a quoted key in destructuring.

Example pattern:
```ts
function isHyphenatedJsxProp(originalName: string): boolean {
  return !isValidIdentifier(originalName) && /^[a-zA-Z_][\w.-]*$/.test(originalName);
}

// If hyphenated: keep original name in call site; destructure via quoted key
// const { 'aria-label': ariaLabel } = temp;
// Otherwise: destructure via identifier binding
// const { key } = temp;
```

Also, keep comments consistent with invariants (e.g., “valid identifiers only”) rather than implying broader acceptance than the parser allows.