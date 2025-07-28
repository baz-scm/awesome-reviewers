---
title: Fail fast explicitly
description: When critical components or operations fail, throw explicit errors rather
  than silently continuing or returning nil. Silent failures can mislead users into
  thinking operations succeeded when they didn't, potentially causing data loss or
  inconsistent application state.
repository: logseq/logseq
label: Error Handling
language: Other
comments_count: 4
repository_stars: 37695
---

When critical components or operations fail, throw explicit errors rather than silently continuing or returning nil. Silent failures can mislead users into thinking operations succeeded when they didn't, potentially causing data loss or inconsistent application state.

Key principles:
- Throw explicit errors when required dependencies are missing (e.g., database workers, required parameters)
- Avoid catch-all handlers that suppress errors without proper handling
- Use meaningful error messages that help users understand what went wrong
- Prefer failing fast over graceful degradation when data integrity is at risk

Example of problematic silent failure:
```clojure
(when-let [^Object sqlite @db-browser/*worker]
  ;; operation continues only if worker exists
  ;; but silently does nothing if worker is nil
  (.transact sqlite repo tx-data tx-meta))
```

Better approach with explicit failure:
```clojure
(if-let [^Object sqlite @db-browser/*worker]
  (.transact sqlite repo tx-data tx-meta)
  (throw (js/Error. "Database worker not initialized - data cannot be persisted")))
```

This prevents users from losing data silently and makes debugging easier by surfacing issues immediately rather than allowing them to compound.