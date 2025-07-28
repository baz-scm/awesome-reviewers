---
title: Multi-arity backward compatibility
description: When extending existing API functions with new parameters, use multi-arity
  function definitions to maintain backward compatibility. This allows existing code
  to continue working unchanged while providing enhanced functionality through additional
  arities.
repository: logseq/logseq
label: API
language: Other
comments_count: 3
repository_stars: 37695
---

When extending existing API functions with new parameters, use multi-arity function definitions to maintain backward compatibility. This allows existing code to continue working unchanged while providing enhanced functionality through additional arities.

The pattern involves defining the original function signature that delegates to the extended version with default values, then defining the extended signature with the new parameters. This approach prevents breaking changes for existing callers while enabling new functionality.

Example implementation:
```clojure
(defn eval-string
  ([s]
   (eval-string s {}))
  ([s ns]
   (try
     (sci/eval-string s {:bindings {'sum sum
                                    'average average}
                        :namespaces ns}))))

(defn resolve-input
  ([input]
   (resolve-input input nil))
  ([input current-block-uuid]
   (cond
     (= :current-block input)
     (when current-block-uuid
       (some-block-lookup current-block-uuid))
     :else input)))
```

This pattern is especially important for APIs used by external consumers like plugins, where breaking changes can cause widespread compatibility issues. Always validate that the default parameter values work correctly across all intended usage contexts.