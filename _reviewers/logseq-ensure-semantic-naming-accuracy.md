---
title: Ensure semantic naming accuracy
description: Names should accurately reflect the actual behavior, purpose, and scope
  of functions, variables, and classes. Misleading or inaccurate names create confusion
  and maintenance burden.
repository: logseq/logseq
label: Naming Conventions
language: Other
comments_count: 9
repository_stars: 37695
---

Names should accurately reflect the actual behavior, purpose, and scope of functions, variables, and classes. Misleading or inaccurate names create confusion and maintenance burden.

Key principles:
- Function names should match their actual behavior, not initial assumptions
- Avoid ambiguous abbreviations that could have multiple meanings
- Choose names that accommodate future extensions rather than overly specific ones
- Use descriptive names over cryptic shortcuts for better maintainability

Examples of improvements:
```clojure
;; Bad: Name suggests uniqueness per view but acts like a type
:logseq.property.view/identity

;; Good: Accurately describes what it represents  
:logseq.property/ui-type

;; Bad: Overly specific, requires changes when extended
:logseq.property/checkbox-default-value

;; Good: Generic enough to support other non-ref types
:logseq.property/scalar-default-value

;; Bad: Ambiguous abbreviation
[frontend.encrypt :as e]  ; could be event, error, etc.

;; Good: Clear and unambiguous
[frontend.encrypt :as encrypt]

;; Bad: Predicate naming convention but returns a key
(defn block-or-page? [id] ...)

;; Good: Either follow predicate convention or use descriptive name
(defn block-or-page-type [id] ...)
```

This prevents bugs caused by incorrect assumptions about functionality and makes code self-documenting for future maintainers.