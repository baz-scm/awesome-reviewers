---
title: Extract reusable hooks
description: When you identify React logic that handles complex state management or
  event handling patterns that could be reused across multiple components, extract
  it into a custom hook. This promotes code reusability, reduces duplication, and
  makes components more focused on their primary responsibilities.
repository: logseq/logseq
label: React
language: Other
comments_count: 2
repository_stars: 37695
---

When you identify React logic that handles complex state management or event handling patterns that could be reused across multiple components, extract it into a custom hook. This promotes code reusability, reduces duplication, and makes components more focused on their primary responsibilities.

For example, IME (Input Method Editor) composition handling is a common pattern that should be extracted:

```clojure
(defn use-ime-composition []
  (let [*composing? (rum/use-ref false)]
    {:composing? (rum/deref *composing?)
     :on-composition-start #(rum/set-ref! *composing? true)
     :on-composition-end #(rum/set-ref! *composing? false)}))

;; Usage in component:
(rum/defc search-input [q matches]
  (let [{:keys [composing? on-composition-start on-composition-end]} (use-ime-composition)
        on-change-fn (fn [e]
                       (let [value (util/evalue e)
                             e-type (gobj/getValueByKeys e "type")]
                         (cond (= e-type "compositionstart") (on-composition-start)
                               (= e-type "compositionend") (on-composition-end))
                         (when-not composing?
                           (debounced-search))))]
    ;; component JSX...
    ))
```

This approach also helps identify and eliminate redundant local state when the same functionality is already handled by other mechanisms like global state updates or component properties.