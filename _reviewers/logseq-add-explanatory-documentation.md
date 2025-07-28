---
title: Add explanatory documentation
description: Add docstrings to functions and comments to explain complex logic, especially
  when the purpose or reasoning isn't immediately clear from the code itself. This
  includes documenting function parameters, explaining non-obvious conditions, and
  clarifying implementation decisions or workarounds.
repository: logseq/logseq
label: Documentation
language: Other
comments_count: 6
repository_stars: 37695
---

Add docstrings to functions and comments to explain complex logic, especially when the purpose or reasoning isn't immediately clear from the code itself. This includes documenting function parameters, explaining non-obvious conditions, and clarifying implementation decisions or workarounds.

Functions should have docstrings that explain their purpose and parameters:

```clojure
(defn convert-index
  "Converts a numeric index to different formats based on delta value.
   Args:
     idx - numeric index to convert
     delta - format selector (0=numeric, 1=letters, else=roman)"
  [idx delta]
  (cond
    (zero? delta) idx
    (= delta 1) (some-> (util/convert-to-letters idx) util/safe-lower-case)
    :else (util/convert-to-roman idx)))
```

Complex conditions and workarounds should be explained with comments:

```clojure
;; hovering on page ref in page-preview does not show another page-preview 
;; if {:preview? true} was passed to page-blocks-cp
(page-reference false page {:preview? true} nil)

;; Check if edit input exists to prevent navigation when not editing
(not (state/get-edit-input-id))
```

Configuration options should include clear explanations and usage examples, especially for potentially risky settings or complex features.