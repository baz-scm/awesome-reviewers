---
title: Defer expensive operations
description: Avoid performing expensive computations until they are actually needed,
  and eliminate redundant work in hot code paths. This includes delaying database
  pulls, moving expensive object creation outside functions, and removing unnecessary
  operations.
repository: logseq/logseq
label: Performance Optimization
language: Other
comments_count: 5
repository_stars: 37695
---

Avoid performing expensive computations until they are actually needed, and eliminate redundant work in hot code paths. This includes delaying database pulls, moving expensive object creation outside functions, and removing unnecessary operations.

Key strategies:
- **Delay expensive operations**: Only perform costly operations like database pulls when actually needed, especially in exception/error branches
- **Hoist expensive computations**: Move expensive object creation (like compiled regexes, composed functions) outside of frequently called functions
- **Use `defonce` for static values**: For expensive computations that produce static results, use `defonce` to avoid recomputation
- **Eliminate redundant operations**: Remove unnecessary function calls, file system operations, or data transformations

Example of delaying expensive operations:
```clojure
;; Bad - always pulls data even if not used
(let [full-data (d/pull db pattern entity-id)]
  (if error
    (throw (ex-info "Error" {:data full-data}))
    (process full-data)))

;; Good - only pull when needed
(if error
  (let [full-data (d/pull db pattern entity-id)]
    (throw (ex-info "Error" {:data full-data})))
  (process (d/pull db pattern entity-id)))
```

Example of hoisting expensive computations:
```clojure
;; Bad - recreates function on every call
(defn remove-nils [nm]
  (into {} (remove (comp nil? second)) nm))

;; Good - create function once
(def remove-nils
  (let [f (comp nil? second)]
    (fn [nm]
      (into {} (remove f) nm))))
```