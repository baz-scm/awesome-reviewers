---
title: Algorithm structure optimization
description: 'Optimize algorithm structure by separating concerns and using appropriate
  data structures and language features. When implementing algorithms:


  1. **Separate search from processing** to improve readability and maintainability.
  When you need to find and process an item, first locate the item, then apply operations
  to it rather than mixing these steps.'
repository: getsentry/sentry
label: Algorithms
language: Python
comments_count: 3
repository_stars: 41297
---

Optimize algorithm structure by separating concerns and using appropriate data structures and language features. When implementing algorithms:

1. **Separate search from processing** to improve readability and maintainability. When you need to find and process an item, first locate the item, then apply operations to it rather than mixing these steps.

2. **Use specialized data structures** that match your algorithm's needs instead of forcing operations into generic containers. Custom structures can combine related data for clearer intent and fewer traversals.

3. **Leverage built-in operations** like set intersections, comprehensions, or functional approaches instead of writing manual loops when possible.

Example of separating search from processing using functional approach:

```python
# Instead of this:
for condition in evidence_data.conditions:
    if condition["condition_result"] == target_priority:
        threshold_type = fetch_threshold_type(Condition(condition["type"]))
        resolve_threshold = fetch_resolve_threshold(condition["comparison"], group_status)
        # More processing...
        break
else:
    raise ValueError("No threshold type found for metric issues")

# Do this:
try:
    condition = next(
        cond for cond in evidence_data.conditions 
        if cond["condition_result"] == target_priority
    )
    threshold_type = fetch_threshold_type(Condition(condition["type"]))
    resolve_threshold = fetch_resolve_threshold(condition["comparison"], group_status)
    # More processing...
except StopIteration:
    raise ValueError("No threshold type found for metric issues")
```

Similarly, for set operations, use the built-in methods rather than explicit iteration:

```python
# Instead of checking each element individually:
workflow_triggers = set()
for dcg in groups_to_fire[group.id]:
    if dcg.id in trigger_group_to_dcg_model[DataConditionHandler.Group.WORKFLOW_TRIGGER]:
        workflow_triggers.add(dcg)

# Do this:
workflow_triggers = groups_to_fire[group.id].intersection(
    trigger_group_to_dcg_model[DataConditionHandler.Group.WORKFLOW_TRIGGER]
)
```