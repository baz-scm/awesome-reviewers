---
title: Identifier and Predicate Naming
description: "Use naming that matches both meaning and mechanics:\n\n- **Generated\
  \ identifiers (transforms/codegen):**\n  - If the source name is meaningful and\
  \ valid in its target position (e.g. JSX attribute name) but not a valid JS identifier,\
  \ **preserve the original name at the call site** and use **quoted keys** for destructuring."
repository: facebook/react#b4
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 251885
---

Use naming that matches both meaning and mechanics:

- **Generated identifiers (transforms/codegen):**
  - If the source name is meaningful and valid in its target position (e.g. JSX attribute name) but not a valid JS identifier, **preserve the original name at the call site** and use **quoted keys** for destructuring.
  - If you must sanitize, do it **deterministically** into valid identifiers and ensure **collision safety** using the correct deduplication boundary (don’t rely on uid generators that may overreact to unrelated outer-scope names).

  Example pattern:
  ```ts
  function isHyphenatedJsxProp(originalName: string): boolean {
    return !isValidIdentifier(originalName) && /^[a-zA-Z_][\w.-]*$/.test(originalName);
  }

  // If isHyphenatedJsxProp("aria-label"), keep "aria-label" in the call site
  // and destructure with a quoted key.
  // const { "aria-label": ariaLabel } = t0;
  ```

- **Boolean predicate helpers:**
  - When a method checks **any/all** over multiple details, the name must reflect that intent.
  - Prefer `hasX`/`hasAnyX` (or an `isX` that clearly implements “exists any”) when the method returns true if **at least one** element matches.

  Example pattern:
  ```ts
  // Semantically “exists at least one detail with severity Error”
  isError(): boolean {
    return this.details.some(d => d.severity === ErrorSeverity.Error);
  }
  ```