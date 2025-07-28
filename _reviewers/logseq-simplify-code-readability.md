---
title: Simplify code readability
description: 'Write code that prioritizes clarity and simplicity over cleverness.
  Use appropriate Clojure idioms to make code more readable and maintainable.


  Key practices:'
repository: logseq/logseq
label: Code Style
language: Other
comments_count: 7
repository_stars: 37695
---

Write code that prioritizes clarity and simplicity over cleverness. Use appropriate Clojure idioms to make code more readable and maintainable.

Key practices:
- Use thread macros (->> ->) to make data transformations easier to follow
- Simplify conditional logic with descriptive let bindings instead of complex nested expressions
- Avoid unnecessary function nesting (e.g., nested `str` calls)
- Choose semantic functions that clearly express intent (`seq` vs `not-empty`)
- Eliminate unnecessary complexity like `delay` when simpler alternatives exist

Example of improvement:
```clojure
;; Instead of complex nested logic:
{:visibility (if (or (not can-open?) (and @*highlight-mode? new?)) "hidden" "visible")}

;; Use descriptive let bindings:
(let [is-new-highlight (and selection @*highlight-mode? new?)
      is-existing-highlight (and selection @*highlight-mode? (not new?))
      should-display-for-new-highlight (and is-new-highlight (state/sub :pdf/auto-open-ctx-menu?))]
  {:visibility (if (or is-existing-highlight should-display-for-new-highlight) "visible" "hidden")})

;; Instead of nested function calls:
(str (string/join ", " (map name (keys (:plugin/installed-plugins @state/state)))))

;; Use thread macros for clarity:
(->> (:plugin/installed-plugins @state/state)
     keys
     (map name)
     (string/join ", "))
```

This approach makes code more maintainable, especially for team members who may not be familiar with complex Clojure patterns, and reduces cognitive load when reading and debugging code.