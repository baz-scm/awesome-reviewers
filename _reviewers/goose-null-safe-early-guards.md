---
title: Null-safe early Guards
description: Always handle nullable/optional state explicitly before executing logic
  that can mutate state, clear user input, or drop data. Use early returns or dedicated
  “disabled” props driven by well-defined nullable/flag conditions, and preserve intentional
  empty values instead of treating all falsy/empty inputs as “missing.”
repository: aaif-goose/goose
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 51876
---

Always handle nullable/optional state explicitly before executing logic that can mutate state, clear user input, or drop data. Use early returns or dedicated “disabled” props driven by well-defined nullable/flag conditions, and preserve intentional empty values instead of treating all falsy/empty inputs as “missing.”

How to apply:
- Guard before side effects: if a required snapshot/session field may be missing or a flag indicates the operation must not proceed, check it up front and return/disable.
- Use dedicated disablement props: drive UI blocking with a specific boolean (not a loosely related one) so tooltips/side effects match the real null-handling reason.
- Preserve empty collections/data: when stripping/transforming params, keep empty arrays if they’re semantically meaningful. When filtering message content, skip only when both text and images are absent.

Example pattern:
```ts
function onUpdate({ currentSnapshot, updateMessage }: any) {
  // Explicit null/flag guard
  if (!currentSnapshot?.session || currentSnapshot.session.working_dir_missing === true) {
    return; // block side effects when required data is missing
  }

  updateMessage();
}

function stripEmptySlots(params: Record<string, any>) {
  for (const [key, value] of Object.entries(params)) {
    const isEmptyObject =
      value && typeof value === 'object' && !Array.isArray(value) && Object.keys(value).length === 0;
    if (isEmptyObject) delete params[key];
    // Note: empty arrays are preserved
  }
}
```