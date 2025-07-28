---
title: Separate user system data
description: Separate user-facing data from system/implementation data using proper
  namespacing and schema design to prevent data pollution and improve user experience.
repository: logseq/logseq
label: Database
language: Other
comments_count: 4
repository_stars: 37695
---

Separate user-facing data from system/implementation data using proper namespacing and schema design to prevent data pollution and improve user experience.

System-generated properties, internal attributes, and feature-specific data should be clearly separated from user-accessible data through namespacing or dedicated attributes. This prevents implementation details from appearing in user interfaces like autocompletion, queries, and property dropdowns.

**Implementation approaches:**
1. **Namespace system properties**: Use prefixed namespaces for feature-specific data
2. **Hide internal attributes**: Mark implementation details as non-public and hidden
3. **Scope data appropriately**: Store configuration at the correct level (graph-level vs global)

**Example - Whiteboard properties separation:**
```clojure
;; Bad - mixes user and system data
{:block/properties 
 {:user-title "My Note"
  :id "system-generated-id"  ; system data pollutes user space
  :fill "black"              ; tldraw-specific
  :stroke "#ababab"}}        ; tldraw-specific

;; Good - namespaced separation  
{:block/properties
 {:user-title "My Note"
  :logseq.tldraw.shape {:id "system-generated-id"
                        :fill "black" 
                        :stroke "#ababab"}}}
```

**Example - Internal attribute hiding:**
```clojure
:block/order {:title "Node order"
              :attribute :block/order  
              :schema {:type :string
                       :public? false    ; Hidden from user queries
                       :hide? true}}     ; Hidden from autocompletion
```

This separation improves query performance, prevents user confusion, and makes the system more maintainable by clearly delineating data boundaries.