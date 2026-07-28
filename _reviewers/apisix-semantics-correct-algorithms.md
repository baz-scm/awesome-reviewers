---
title: Semantics-Correct Algorithms
description: When implementing or choosing an algorithm (scoring, aggregation, throttling,
  parsing), ensure it matches the domain semantics and behaves predictably under edge
  cases.
repository: apache/apisix
label: Algorithms
language: Other
comments_count: 4
repository_stars: 16922
---

When implementing or choosing an algorithm (scoring, aggregation, throttling, parsing), ensure it matches the domain semantics and behaves predictably under edge cases.

Guidelines:
- Match the meaning of inputs to the reduction/selection operator. If the decision should succeed when *any* candidate matches, use `max`-style logic; avoid `avg/min`-style dilution unless the semantics truly require “all” or “average.”
- Avoid “knobs” that enable semantically incorrect defaults. Prefer a single safe behavior (or document loudly why each option changes routing/throttling outcomes).
- When offering exact vs approximate algorithms, make the trade-off explicit and bounded:
  - Exact algorithms: justify complexity/space and show why state doesn’t grow unbounded.
  - Approximate algorithms: quantify error expectations and document intended use cases.
- Ensure deterministic behavior where order matters (e.g., sorting names before returning) and make parsing robust to legal trailing frames/comments/heartbeats.
- Add targeted tests that demonstrate correctness (including numeric counterexamples and realistic protocol edge cases).

Example (semantic routing aggregation):
```lua
-- Scores are for alternative examples of the same intent.
-- Semantics: “any example matches => route succeeds”, so aggregate by max.
local function semantic_pick(scores, threshold)
    local best = -math.huge
    for _, s in ipairs(scores) do
        if s > best then best = s end
    end
    if best >= threshold then
        return true
    end
    return false
end
```

Apply this standard whenever you change scoring/routing/throttling/parsing logic, especially for user-visible behavior where “almost right” algorithms cause silent misroutes or inconsistent rate-limit outcomes.