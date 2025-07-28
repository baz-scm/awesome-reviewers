---
title: Filter nil values defensively
description: Proactively filter out nil values from collections and validate non-empty
  states before processing to prevent runtime errors. This defensive approach prevents
  common issues like "Cannot read properties of null" errors and ensures robust data
  handling.
repository: logseq/logseq
label: Null Handling
language: Other
comments_count: 3
repository_stars: 37695
---

Proactively filter out nil values from collections and validate non-empty states before processing to prevent runtime errors. This defensive approach prevents common issues like "Cannot read properties of null" errors and ensures robust data handling.

When working with collections that may contain nil values, filter them out before processing:

```clojure
;; Before: Risk of null pointer errors
(let [blocks (util/sort-by-height blocks)]
  ...)

;; After: Safe processing
(let [blocks (util/sort-by-height (remove nil? blocks))]
  ...)
```

Use `seq` instead of `seq?` to check for non-empty collections:

```clojure
;; Check if collection has content before processing
(when (seq paths)
  ;; Process paths safely
  ...)
```

While this pattern requires callers to handle nil states (leading to `(remove nil?)` throughout the codebase), it prevents more serious downstream errors and makes error handling explicit rather than allowing silent failures or confusing secondary errors.